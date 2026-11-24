# Tailscale Tray Controller — Implementation Plan

## Goal

Create a small Linux Mint system-tray application for the `stormbase` machine that
shows whether Tailscale is running and offers the requested profile and network
preference controls.

## Validated local CLI contract

The installed client is Tailscale `1.104.7`. Its relevant commands are:

- `tailscale status --json` for machine/backend state and current preferences.
- `tailscale switch --list --json` to obtain available signed-in accounts, then
  `tailscale switch <id>` to select one.
- `tailscale set --accept-dns=<true|false>` and
  `tailscale set --accept-routes=<true|false>` for independent preferences.

`tailscale switch` is currently marked alpha by the client, so its JSON parser will
be deliberately isolated and covered by saved command-output fixtures.

## Technical shape

- **Language/runtime:** Python 3.
- **Desktop integration:** PyGObject + Ayatana AppIndicator (the maintained
  AppIndicator implementation commonly supported by Linux Mint/Cinnamon).
- **UI model:** a background command/state service drives one tray icon and rebuilds
  the menu from a single immutable status snapshot; GTK/UI updates occur only on the
  main loop.
- **Packaging:** a local Python virtual environment or distro package dependencies,
  a `.desktop` autostart entry, and an application icon set. Keep the first release
  local-only; do not add a daemon, web service, database, or network listener.

## Privilege approach

The application must never use a shell or interpolate profile names into commands.
It will invoke the `tailscale` executable with an argument array and capture stdout,
stderr, exit status, and a timeout.

Preferred setup is a one-time, user-approved administrator command:

```bash
sudo tailscale set --operator="$USER"
```

That delegates routine Tailscale CLI operation to the desktop user, removing password
prompts from ordinary menu clicks. The setup checker will detect whether ordinary
`tailscale status --json` works and show a clear “grant operator access” recovery item
when it does not. It will not silently run `sudo`, cache a password, or write a broad
sudoers rule. If the user declines operator access, the app remains read-only and
explains that administrator configuration is required for actions.

## User experience

1. Start on login; run an immediate non-privileged status refresh and repeat every
   10 seconds (plus after any command completes).
2. Show a **green** icon when the Tailscale backend is `Running`; show **red** when it
   is stopped, unavailable, logged out, or an error prevents status retrieval. Include
   an accessible tooltip with the precise state/reason rather than relying on color.
3. The menu shows current state and account, followed by:
   - **Start Tailscale** / **Stop Tailscale** — a state-labelled checkable item that
     runs `tailscale up` or `tailscale down`, then confirms the resulting state.
   - **Switch workspace…** — fetch `tailscale switch --list --json`, present each
     profile in a picker dialog, mark the active profile, and run `tailscale switch
     <id>` only after a selection. Disable it whenever Tailscale is not running.
   - **Accept DNS** — a checkable item mapped to the observed `AcceptDNS` preference;
     clicking it runs `tailscale set --accept-dns=true|false`.
   - **Accept routes** — equivalent checkable item using `AcceptRoutes` and
     `tailscale set --accept-routes=true|false`.
   - **Refresh**, **Open diagnostics** (recent command/result view), and **Quit**.
4. Disable state-changing items while a command is active. On success, refresh and
   update the menu; on failure, preserve the last confirmed state and surface the
   command’s safe, actionable error text through a desktop notification/diagnostics
   view.
   Keep workspace, DNS, and route controls disabled whenever the backend is stopped;
   `tailscale up` does not apply or overwrite either preference.
   Allow a longer command timeout for workspace switching because the Tailscale CLI
   waits for the selected profile to settle before it exits.

## Build sequence

1. Bootstrap the Python project, dependency declaration, launcher, and basic
   AppIndicator shell. Add monochrome/icon-theme-compatible green/red status assets
   with tooltip and keyboard-accessible menu labels.
2. Implement a `TailscaleClient` boundary using `subprocess.run(..., shell=False)`:
   status parsing, workspace listing/switching, preference updates, normalized errors,
   and timeouts. Do not let UI code invoke commands directly.
3. Define typed status/profile/preference models and a polling controller that prevents
   overlapping refreshes, applies updates on the GTK main thread, and retains the last
   known-good snapshot.
4. Build the dynamic menu and action state machine. Treat profile data as display text
   only and pass the exact parsed profile ID as one argument to the client boundary.
5. Add the permission/setup detector and read-only failure state. Document the
   one-time operator setup, how to undo it, and the security trade-off.
6. Add unit tests with recorded JSON fixtures for running/stopped/logged-out states,
   malformed CLI output, workspace-list variations, command failures, menu enablement,
   and both preference toggles. Add a lightweight manual Linux Mint smoke-test script.
7. Add installation/autostart documentation and validate launch, status transitions,
   switching, DNS/routes updates, and recovery from `tailscaled` stopping/restarting.

## Acceptance checks

- The icon and tooltip transition from red to green within one polling interval after
  Tailscale reaches `Running`, and return to red after it stops.
- The menu reflects the active account and preference values from fresh status data.
- Selecting a listed workspace issues exactly `tailscale switch <selected-id>`.
- Each toggle changes only its corresponding flag and refreshes to confirm the result.
- Unavailable privilege, daemon, malformed output, and non-zero CLI exits do not crash
  the tray app or falsely show a successful change.
- No action uses `shell=True`, writes passwords, or grants broad command access.

## Decisions deferred until implementation

- Exact icon artwork (use system-theme symbolic icons first unless custom branding is
  requested).
- Whether to ship a native distro package; the first pass can be run from the project
  directory with a `.desktop` launcher.
- Whether a later release should expose start/stop/logout controls; they are explicitly
  out of scope for this requested minimum application.
