# Codex Session Instructions

If you restart Codex and need to continue this project:

- Project root: `/home/user/Documents/projects/starter`
- Target: postmarketOS GTK4/libadwaita app named `Jaraco Starter`
- Config path: `~/.config/jaraco/starter.json`
- Config format: JSON with `actions[]` and fields `name`, `script`, `sudo`
- UI: radio buttons `Off` / `On` with labels to the right
- Behavior:
  - `On` executes the script (using `pkexec` if `sudo: true`)
  - `Off` kills the exact PID started by `On` (SIGTERM, then SIGKILL after 3s)
- Sample config: `starter.sample.json` uses `/usr/bin/tor`
- Auto-seed config on first run:
  - copy `/usr/share/jaraco-starter/starter.sample.json` to `~/.config/jaraco/starter.json`
  - if sample missing, write a default tor config
- Packaging: `APKBUILD` + `Makefile`
  - `make dist` creates `dist/jaraco-starter-0.1.0.tar.gz`
  - `abuild checksum` updates APKBUILD sums
  - `make abuild` builds the APK
- Build status:
  - `abuild` works but failed because current shell lacked `abuild` group membership
  - `newgrp abuild` failed with "Operation not permitted"
  - Need a fresh login session to pick up `abuild` group, then rerun `make abuild`

