import argparse
import errno
import signal
import subprocess
from types import SimpleNamespace

import pytest

from jaraco_starter import runner


def test_start_process_prints_process_group_id(monkeypatch, capsys):
    popen_calls = {}

    class DummyProc:
        pid = 4321

    def fake_popen(argv, **kwargs):
        popen_calls["argv"] = argv
        popen_calls["kwargs"] = kwargs
        return DummyProc()

    monkeypatch.setattr(runner.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(runner.os, "getpgid", lambda pid: pid + 10)

    rc = runner._start_process(["/bin/echo", "hello"])

    assert rc == 0
    assert popen_calls["argv"] == ["/bin/echo", "hello"]
    assert popen_calls["kwargs"]["preexec_fn"] is runner.os.setsid
    assert popen_calls["kwargs"]["stdin"] is subprocess.DEVNULL
    assert popen_calls["kwargs"]["stdout"] is subprocess.DEVNULL
    assert popen_calls["kwargs"]["stderr"] is subprocess.DEVNULL
    assert popen_calls["kwargs"]["close_fds"] is True
    assert capsys.readouterr().out.strip() == "4331"


def test_is_group_alive_false_when_process_missing(monkeypatch):
    def fake_killpg(_pgid, _sig):
        raise ProcessLookupError

    monkeypatch.setattr(runner.os, "killpg", fake_killpg)

    assert runner._is_group_alive(100) is False


def test_is_group_alive_true_on_permission_error(monkeypatch):
    def fake_killpg(_pgid, _sig):
        raise PermissionError

    monkeypatch.setattr(runner.os, "killpg", fake_killpg)

    assert runner._is_group_alive(100) is True


def test_kill_group_returns_zero_when_group_missing(monkeypatch):
    def fake_killpg(_pgid, _sig):
        raise ProcessLookupError

    monkeypatch.setattr(runner.os, "killpg", fake_killpg)

    assert runner._kill_group(321, 0.1) == 0


def test_kill_group_escalates_to_sigkill(monkeypatch):
    calls = []
    times = iter([100.0, 100.0, 100.05, 100.11])

    def fake_killpg(pgid, sig):
        calls.append((pgid, sig))

    monkeypatch.setattr(runner.os, "killpg", fake_killpg)
    monkeypatch.setattr(runner, "_is_group_alive", lambda _pgid: True)
    monkeypatch.setattr(runner.time, "time", lambda: next(times))
    monkeypatch.setattr(runner.time, "sleep", lambda _seconds: None)

    assert runner._kill_group(321, 0.1) == 0
    assert calls == [(321, signal.SIGTERM), (321, signal.SIGKILL)]


def test_kill_group_stops_after_process_exits(monkeypatch):
    calls = []
    states = iter([True, False])
    times = iter([100.0, 100.0, 100.05])

    def fake_killpg(pgid, sig):
        calls.append((pgid, sig))

    monkeypatch.setattr(runner.os, "killpg", fake_killpg)
    monkeypatch.setattr(runner, "_is_group_alive", lambda _pgid: next(states))
    monkeypatch.setattr(runner.time, "time", lambda: next(times))
    monkeypatch.setattr(runner.time, "sleep", lambda _seconds: None)

    assert runner._kill_group(321, 0.5) == 0
    assert calls == [(321, signal.SIGTERM)]


def test_cmd_run_delegates_to_start_process(monkeypatch):
    captured = {}

    def fake_start_process(argv):
        captured["argv"] = argv
        return 7

    monkeypatch.setattr(runner, "_start_process", fake_start_process)

    rc = runner.cmd_run(SimpleNamespace(command=["python3", "-V"]))

    assert rc == 7
    assert captured["argv"] == ["python3", "-V"]


def test_cmd_shell_wraps_command_in_sh(monkeypatch):
    captured = {}

    def fake_start_process(argv):
        captured["argv"] = argv
        return 9

    monkeypatch.setattr(runner, "_start_process", fake_start_process)

    rc = runner.cmd_shell(SimpleNamespace(command="echo hello"))

    assert rc == 9
    assert captured["argv"] == ["/bin/sh", "-c", "echo hello"]


def test_cmd_pgrep_uses_exact_matching_by_default(monkeypatch, capsys):
    def fake_run(cmd, **kwargs):
        assert cmd == ["pgrep", "-x", "tor"]
        assert kwargs == {"check": False, "capture_output": True, "text": True}
        return SimpleNamespace(returncode=0, stdout="123\n", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    rc = runner.cmd_pgrep(SimpleNamespace(full=False, pattern="tor"))

    assert rc == 0
    assert capsys.readouterr().out == "123\n"


def test_cmd_pgrep_uses_full_matching_when_requested(monkeypatch):
    def fake_run(cmd, **kwargs):
        assert cmd == ["pgrep", "-f", "python -m http.server"]
        return SimpleNamespace(returncode=1, stdout="", stderr="")

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    assert runner.cmd_pgrep(SimpleNamespace(full=True, pattern="python -m http.server")) == 1


def test_cmd_pgrep_returns_127_when_pgrep_missing(monkeypatch, capsys):
    def fake_run(_cmd, **_kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    rc = runner.cmd_pgrep(SimpleNamespace(full=False, pattern="tor"))

    assert rc == 127
    assert "pgrep not found" in capsys.readouterr().err


def test_cmd_kill_delegates_to_kill_group(monkeypatch):
    captured = {}

    def fake_kill_group(pgid, timeout):
        captured["args"] = (pgid, timeout)
        return 5

    monkeypatch.setattr(runner, "_kill_group", fake_kill_group)

    rc = runner.cmd_kill(SimpleNamespace(pgid=55, timeout=1.25))

    assert rc == 5
    assert captured["args"] == (55, 1.25)


def test_build_parser_supports_all_subcommands():
    parser = runner.build_parser()

    run_args = parser.parse_args(["run", "echo", "hi"])
    shell_args = parser.parse_args(["shell", "echo hi"])
    pgrep_args = parser.parse_args(["pgrep", "--full", "python"])
    kill_args = parser.parse_args(["kill", "12", "--timeout", "0.5"])

    assert run_args.subcommand == "run"
    assert run_args.command == ["echo", "hi"]
    assert shell_args.subcommand == "shell"
    assert shell_args.command == "echo hi"
    assert pgrep_args.subcommand == "pgrep"
    assert pgrep_args.full is True
    assert pgrep_args.pattern == "python"
    assert kill_args.subcommand == "kill"
    assert kill_args.pgid == 12
    assert kill_args.timeout == 0.5


def test_main_rejects_run_without_command():
    with pytest.raises(SystemExit) as exc:
        runner.main(["run"])

    assert exc.value.code == 2


def test_main_returns_127_for_missing_executable(monkeypatch, capsys):
    def fake_start_process(_argv):
        raise OSError(errno.ENOENT, "missing executable")

    monkeypatch.setattr(runner, "_start_process", fake_start_process)

    rc = runner.main(["run", "missing-binary"])

    assert rc == 127
    assert "Executable not found" in capsys.readouterr().err


def test_main_returns_one_for_other_os_errors(monkeypatch, capsys):
    def fake_start_process(_argv):
        raise OSError(errno.EPERM, "permission denied")

    monkeypatch.setattr(runner, "_start_process", fake_start_process)

    rc = runner.main(["run", "blocked"])

    assert rc == 1
    assert "permission denied" in capsys.readouterr().err
