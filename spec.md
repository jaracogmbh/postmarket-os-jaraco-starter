**Jaraco Starter Replication Spec (postmarketOS/Alpine)**

**Ziel**
Eine kleine GTK4/libadwaita‑App, die Actions aus einer JSON‑Konfiguration lädt und diese als On/Off‑Schalter darstellt. Jede Action startet ein Skript (optional mit Root‑Rechten via Polkit) und kann es sauber beenden.

**Funktionale Anforderungen**
- UI zeigt eine Liste von Actions mit Radio‑Buttons `Off` / `On`.
- Konfiguration aus `~/.config/jaraco/starter.json`.
- Actions enthalten `name`, `script`, `sudo` und optional `kill_command`, `kill_sudo`.
- `On` startet das Kommando (bei `sudo: true` via `pkexec`).
- `Off` beendet den exakten Prozess (SIGTERM → 3s warten → SIGKILL).
- Wenn `kill_command` gesetzt ist, wird es bevorzugt zum Stoppen verwendet.
- UI zeigt Fehler via Dialog/Banner.
- Erststart: Sample‑Config in `~/.config/jaraco/starter.json` kopieren, falls nicht vorhanden.

**Nicht‑funktionale Anforderungen**
- Läuft auf postmarketOS (Alpine) mit GTK4/libadwaita.
- Python >= 3.10, PyGObject.
- Polkit‑Integration über `pkexec` und Policy‑Datei.

---

**Projektstruktur**
```
jaraco-starter/
  README.md
  pyproject.toml
  setup.py
  starter.sample.json
  src/
    jaraco_starter/
      __init__.py
      app.py
      runner.py
  data/
    io.jaraco.Starter.desktop
    io.jaraco.Starter.metainfo.xml
    io.jaraco.Starter.svg
    io.jaraco.Starter.policy
  APKBUILD
  Makefile
```

---

**Beispiel‑Konfiguration** (`~/.config/jaraco/starter.json`)
```json
{
  "actions": [
    {
      "name": "Tor",
      "script": "/usr/bin/tor",
      "sudo": true
    },
    {
      "name": "Notes Sync",
      "script": "/home/user/bin/notes-sync.sh",
      "sudo": false
    }
  ]
}
```

Optional pro Action:
- `kill_command`: z. B. `/usr/bin/pkill -f /usr/bin/tor`
- `kill_sudo`: überschreibt `sudo` für den Kill‑Befehl

---

**Benötigte Pakete (Alpine/postmarketOS)**
Aus `APKBUILD`:
- `python3`
- `py3-gobject3`
- `gtk4.0`
- `libadwaita`
- `polkit`

Build‑Deps:
- `py3-setuptools`

---

**Installations‑Check (Alpine, ohne doppeltes Installieren)**
Verwende `apk info -e` vor dem Install:
```sh
required="python3 py3-gobject3 gtk4.0 libadwaita polkit"
for pkg in $required; do
  if apk info -e "$pkg" >/dev/null 2>&1; then
    echo "OK: $pkg ist bereits installiert"
  else
    echo "Installiere: $pkg"
    sudo apk add "$pkg"
  fi
done
```

Für Build‑Tools:
```sh
if ! apk info -e py3-setuptools >/dev/null 2>&1; then
  sudo apk add py3-setuptools
fi
```

---

**Kern‑Implementierung**

**Wesentliche Detail‑Logik (für 1:1 Replikation)**
- App‑ID ist `io.jaraco.Starter` (GTK/Adw Application ID, Desktop‑ID, Icon‑Name, Metainfo‑ID).
- `CONFIG_PATH` ist `~/.config/jaraco/starter.json` (expanduser).
- `SAMPLE_PATH` ist `/usr/share/jaraco-starter/starter.sample.json`.
- **Seeding‑Logik**: Wenn Config fehlt, wird `SAMPLE_PATH` kopiert. Falls Sample fehlt, wird ein Default‑Config‑JSON geschrieben mit einer Tor‑Action inklusive `kill_command` und `kill_sudo: true`.
- **Initialzustand**: Beim Start wird pro Action ein Running‑Check durchgeführt und die `Off`/`On`‑Buttons entsprechend gesetzt.
- **Threading/UI**: Bei Start/Stop mit `sudo` wird der Prozess in einem Worker‑Thread ausgeführt und das UI via `GLib.idle_add` aktualisiert, um UI‑Freeze zu vermeiden.
- **PID‑Semantik**: Der Runner gibt die Prozessgruppen‑ID (PGID) zurück; diese PGID wird für spätere Kill‑Operationen verwendet.
- **Kill‑Semantik**: `SIGTERM` an Prozessgruppe, 3s warten, danach `SIGKILL` an Prozessgruppe, falls noch lebendig.

**Running‑Detection‑Logik**
- Wenn `kill_command` gesetzt ist, wird daraus ein Pattern für `pgrep` abgeleitet.
- Parsing‑Regeln:
  - Strip leading `doas`, `sudo`, `pkexec`.
  - Handle `sh -c` / `/bin/sh -c` und parse den inneren String.
  - `killall <name>` → pattern = `<name>`, `full=false`.
  - `pkill [-f] <pattern>` → pattern = `<pattern>`, `full=true` wenn `-f`.
- Wenn kein `kill_command`: Pattern aus `script` ableiten. Default: basename des ersten Tokens; bei Parsing‑Fehlern `full=true` und Pattern = gesamter String.
- `pgrep` wird ohne sudo als `pgrep -x` (oder `-f`) verwendet; mit sudo über `pkexec /usr/lib/jaraco-starter/runner pgrep [--full] <pattern>`.

**Polkit‑Policy‑Fixpunkte**
- Policy‑Action‑ID ist `io.jaraco.Starter.run`.
- `org.freedesktop.policykit.exec.path` muss exakt `/usr/lib/jaraco-starter/runner` sein.

**1) `app.py` (GUI + Prozesssteuerung)**
- Lädt Config, rendert ListBox‑Rows mit `Off`/`On`.
- Startet Commands via `subprocess.Popen` (ohne sudo) oder via `pkexec` + Runner (mit sudo).
- Stoppt über:
  - `kill_command` (mit optionalem sudo) **oder**
  - `pkexec runner kill <pid>` (sudo‑Fall) **oder**
  - `os.killpg(pid, SIGTERM)` → 3s → `SIGKILL`.
- `pgrep` wird genutzt, um bestehende PIDs zu erkennen.

**2) `runner.py` (privilegierter Helper)**
- Subcommands: `run`, `shell`, `pgrep`, `kill`.
- Gibt PID der Prozessgruppe zurück.
- Wird über Polkit‑Policy freigeschaltet.

---

**Polkit‑Integration**
Datei: `data/io.jaraco.Starter.policy`
- `org.freedesktop.policykit.exec.path` zeigt auf `/usr/lib/jaraco-starter/runner`.
- Standard: `auth_admin_keep`.

---

**Desktop‑Integration**
Dateien in `data/`:
- `io.jaraco.Starter.desktop`
- `io.jaraco.Starter.metainfo.xml`
- `io.jaraco.Starter.svg`

---

**Packaging (APKBUILD)**
- `python3 setup.py install --root="$pkgdir" --prefix=/usr`
- `runner.py` nach `/usr/lib/jaraco-starter/runner`
- Polkit‑Policy nach `/usr/share/polkit-1/actions/`
- Desktop‑Dateien nach `/usr/share/applications/` und `/usr/share/metainfo/`
- Icon nach `/usr/share/icons/hicolor/scalable/apps/`
- Sample‑Config nach `/usr/share/jaraco-starter/starter.sample.json`

---

**Build‑/Install‑Ablauf (postmarketOS)**
```sh
# Tarball erstellen
make dist

# APK bauen
make abuild
```

Optional lokale Sample‑Config:
```sh
make install-sample
```

---

**Laufzeit‑Verhalten**
- Bei Start ohne Config wird `starter.sample.json` kopiert.
- Start‑Fehler zeigen einen Dialog.
- Stop‑Fehler reaktivieren den `On`‑Button.

---

**Validierung**
- App startet ohne Config → Config wird erzeugt.
- `On` startet Skript, `Off` stoppt es sauber.
- `sudo`‑Actions fordern Authentifizierung via Polkit an.
- `kill_command` überschreibt PID‑Kill.
