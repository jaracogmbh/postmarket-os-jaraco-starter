# Jaraco Starter

Small GTK4/libadwaita app for postmarketOS that renders actions from a JSON
config and starts or stops the associated scripts.

## Config

Config file path:

```
~/.config/jaraco/starter.json
```

Example:

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

Notes:
- Scripts must be executable and include a shebang.
- If `sudo` is `true`, the app uses `pkexec` with a polkit policy to elevate.
- Turning a row off sends `SIGTERM` to the exact PID started for that action.
- If the process does not exit within 3 seconds, it escalates to `SIGKILL`.

Sample config file:

```
starter.sample.json
```
