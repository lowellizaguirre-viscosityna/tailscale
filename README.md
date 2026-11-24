# TailTray

TailTray is a small Linux Mint system-tray controller for the local Tailscale client.
It starts or stops Tailscale, shows its state, switches among signed-in workspaces, and
controls whether Tailscale DNS and advertised routes are accepted.

Workspace selection is available only while Tailscale is running. Selecting it opens a
picker with each saved profile's name, account, and tailnet returned by the local
Tailscale client.

DNS and route checkboxes reflect the active profile's stored `tailscale debug prefs`
values. Starting Tailscale invokes only `tailscale up`; it does not change either
preference. While Tailscale is stopped, workspace, DNS, and route controls are disabled
until the connection is running again. If a newly selected profile comes up stopped,
use **Start Tailscale** first, then open the workspace picker to switch again.

## Install on Linux Mint

Install the desktop bindings and create a project-local environment:

```bash
sudo apt install gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 python3-gi
python3 -m venv .venv --system-site-packages
.venv/bin/pip install --editable .
```

For actions without a password prompt, explicitly delegate Tailscale operations to
your desktop user once:

```bash
sudo tailscale set --operator="$USER"
```

If TailTray reports **prefs write access denied**, run that command from a terminal
owned by the same desktop user, then quit and reopen TailTray. It is a one-time
Tailscale permission setup; the application does not request or retain your password.

Run the application with:

```bash
.venv/bin/tailtray
```

The app never runs `sudo` itself, stores a password, or uses a shell to invoke
Tailscale. Without operator access it remains readable where possible and explains how
to enable controls.
