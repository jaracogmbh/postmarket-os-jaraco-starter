#!/usr/bin/env python3
"""
Privileged helper for jaraco-starter.

Subcommands:
- run <cmd...>            Start command and print PGID.
- shell <command_string>  Start via /bin/sh -c and print PGID.
- pgrep [--full] <pat>    Proxy to pgrep (returns matching PIDs on stdout).
- kill <pgid>             SIGTERM process group, then SIGKILL after timeout.
"""

from __future__ import annotations

import argparse
import errno
import os
import signal
import subprocess
import sys
import time


def _start_process(argv: list[str]) -> int:
    proc = subprocess.Popen(
        argv,
        preexec_fn=os.setsid,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
    )
    pgid = os.getpgid(proc.pid)
    print(pgid)
    return 0


def _is_group_alive(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _kill_group(pgid: int, timeout_s: float) -> int:
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return 0
    except PermissionError as exc:
        print(f"Permission denied while sending SIGTERM to {pgid}: {exc}", file=sys.stderr)
        return 1

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if not _is_group_alive(pgid):
            return 0
        time.sleep(0.1)

    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        return 0
    except PermissionError as exc:
        print(f"Permission denied while sending SIGKILL to {pgid}: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    return _start_process(args.command)


def cmd_shell(args: argparse.Namespace) -> int:
    return _start_process(["/bin/sh", "-c", args.command])


def cmd_pgrep(args: argparse.Namespace) -> int:
    cmd = ["pgrep", "-f" if args.full else "-x", args.pattern]
    try:
        res = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        print("pgrep not found", file=sys.stderr)
        return 127
    if res.stdout:
        sys.stdout.write(res.stdout)
    if res.stderr:
        sys.stderr.write(res.stderr)
    return res.returncode


def cmd_kill(args: argparse.Namespace) -> int:
    return _kill_group(args.pgid, args.timeout)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="runner")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    p_run = subparsers.add_parser("run", help="Run command and print PGID")
    p_run.add_argument("command", nargs=argparse.REMAINDER)
    p_run.set_defaults(func=cmd_run)

    p_shell = subparsers.add_parser("shell", help="Run shell command and print PGID")
    p_shell.add_argument("command")
    p_shell.set_defaults(func=cmd_shell)

    p_pgrep = subparsers.add_parser("pgrep", help="Find process IDs")
    p_pgrep.add_argument("--full", action="store_true", help="Match against full command line")
    p_pgrep.add_argument("pattern")
    p_pgrep.set_defaults(func=cmd_pgrep)

    p_kill = subparsers.add_parser("kill", help="Stop process group by PGID")
    p_kill.add_argument("pgid", type=int)
    p_kill.add_argument("--timeout", type=float, default=3.0)
    p_kill.set_defaults(func=cmd_kill)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.subcommand == "run" and not args.command:
        parser.error("run requires a command")

    try:
        return int(args.func(args))
    except OSError as exc:
        if exc.errno == errno.ENOENT:
            print(f"Executable not found: {exc}", file=sys.stderr)
            return 127
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

