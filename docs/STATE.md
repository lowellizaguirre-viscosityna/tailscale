# Project State

> The present tense of this project. Overwrite this file at the end of each session
> so it's always true *right now*. History goes in [JOURNAL.md](JOURNAL.md), not here.

**Last updated:** 2026-11-24

## What this project is

_One or two sentences: what it does and who it's for. Fill in at bootstrap._

This project will be a small Linux Mint tray controller for the local Tailscale client
on `stormbase`. It will display connection state, switch among signed-in workspaces,
and toggle DNS and route acceptance.

## Current focus

_What we're working on right now._

- The initial TailTray implementation is complete: Python command layer, GTK/Ayatana
  tray shell, green/red icons, state-labelled start/stop control, running-only workspace
  picker, DNS/routes controls, autostart launcher, and unit tests.
- The command layer uses argument arrays only and was tested against mocked output plus
  this host's unavailable daemon path.
- This workspace lacks PyGObject/Ayatana and the local socket is inaccessible, so the
  visible tray UI and successful privileged actions still need a Linux Mint smoke test.
- DNS/routes state is now read from `tailscale debug prefs` rather than status JSON, and
  workspace labels use the current switch JSON schema's nickname/account/tailnet fields.
- The start/stop and preference actions snapshot the clicked checkbox state before the
  menu is rebuilt; workspace, DNS, and route controls stay disabled while stopped.
- Workspace commands may take longer while a target profile settles; TailTray allows 45
  seconds. A switched-to profile that is stopped must be started before it can switch
  again, matching the stopped-state control rule.
- Permission-denied command responses are translated to explicit operator-access setup
  guidance; TailTray never invokes sudo or stores a password.
- TailTray is registered in `/home/lowell/.config/autostart/tailtray.desktop` and will
  launch after the user's next graphical login or reboot.
- An on-demand launcher is installed at
  `/home/lowell/.local/share/applications/tailtray.desktop` for the application menu.

## Next steps

_The concrete things to do next, in order. The first thing you'd pick up._

1. Install the documented Linux Mint GTK/Ayatana dependencies, create the project venv,
   and launch TailTray manually.
2. If desired, run the explicit one-time Tailscale operator setup, then validate the
   workspace and preference actions against the live daemon.
3. Copy the desktop file to the user's autostart directory after manual validation.

## Open questions

_Unresolved things that need a human or more info. Nothing blocked silently._

- Confirm the preferred installation path (project-local launcher versus distro package).
- Confirm whether the locally observed `tailscale switch --list --json` output matches
  the parser's supported profile shapes; the command remains alpha upstream.

## How to run / work with it

_Commands to build, test, run. Keep this accurate — it's the first thing you'll forget._

- `PYTHONPATH=src python3 -m unittest discover -s tests -v` runs the command-layer tests.
- See the root `README.md` for Linux Mint installation, launch, and autostart steps.
