# Changelog

> **End-user** changelog: what changed, in plain language, newest first. Every entry is
> timestamped. This file is written so it can be surfaced *inside the application* (an
> "What's new" screen, a release-notes page) — keep it free of jargon, file names, and
> internal detail. The developer-facing counterpart is [CHANGELOG-DEV.md](CHANGELOG-DEV.md).

<!-- Add new entries to the TOP. One line per change:

## YYYY-MM-DD HH:MM — Short, plain-language summary

What's different for you, in a sentence or two. No code, no file names.

-->

## 2026-11-24 14:15 — Added an on-demand launcher

You can now find and launch TailTray directly from the Linux Mint application menu.

## 2026-11-24 14:00 — TailTray now starts automatically

TailTray is set to open when you sign in after a reboot, so its status icon is ready
without manually launching the app.

## 2026-11-24 13:45 — Explained Tailscale permission errors

If your account cannot change Tailscale settings yet, the app now explains the one-time
setup needed to enable its controls.

## 2026-11-24 13:30 — Made workspace changes more reliable

Workspace changes now have enough time to finish, and the menu explains how to continue
if the newly selected profile is stopped.

## 2026-11-24 13:15 — Made stopped-state controls safer

Stopping Tailscale now reliably updates the menu, and workspace, DNS, and route
controls remain unavailable until Tailscale is running again.

## 2026-11-24 13:00 — Fixed DNS, routes, and workspace names

DNS and route controls now show their current state, and the workspace picker shows
profile names instead of numeric IDs.

## 2026-11-24 12:45 — Improved start/stop and workspace controls

The menu now says exactly whether it will start or stop Tailscale, and workspace
selection opens a visible picker only when Tailscale is connected.

## 2026-11-24 12:30 — Added a Tailscale start and stop switch

The tray menu can now connect Tailscale when it is stopped and disconnect it when it is
running.

## 2026-11-24 12:15 — Added the Tailscale tray controller

You can now install a local Linux Mint tray app that shows Tailscale status, switches
workspaces, and controls DNS and route acceptance from its menu.

## 2026-11-24 12:00 — Planned the Tailscale tray controller

The project now has a clear plan for a small Linux Mint tray app that shows Tailscale
status, switches workspaces, and controls DNS and route preferences safely.

## 2026-11-18 15:30 — Added a "gates protect operation, not the sandbox" working principle

The assistant's working rules now include a principle that keeps safety and governance
checks from accidentally blocking early development — they apply when real people or
production are involved, not to sandboxed work on test data.

## 2026-11-17 12:20 — Added a project overview

The project now has a README explaining what this template is for and how its files fit
together.

## 2026-11-17 12:00 — Added a dual changelog and shared agent instructions

The project now keeps a running list of changes you can read, and the assistant follows
the same working rules no matter which AI engine is in use.
