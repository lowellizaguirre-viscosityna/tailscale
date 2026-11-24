# Journal

> Append-only log of working sessions, **newest first**. One entry per session.
> Never edit or delete past entries — if something changed, say so in a new entry.
> This is the memory that lets a later session reconstruct how we got here.

<!-- Copy this template to the top for each new entry:

## YYYY-MM-DD — short title

**Did:** what changed this session.
**Why:** the reason / goal behind it.
**Next:** what the following session should pick up (should match STATE.md).
**Notes:** gotchas, dead ends, things that surprised you. Optional.

-->

## 2026-11-24 — Added the TailTray application-menu launcher

**Did:** Installed and validated a user-level desktop entry under
`~/.local/share/applications` that launches TailTray from its project virtual
environment.
**Why:** Autostart handles reboot/login, while a normal desktop entry gives the user an
on-demand application-menu launcher.
**Next:** TailTray can now be launched either on demand or automatically; no project
code work is pending.
**Notes:** The desktop validator's category hint is non-blocking.

## 2026-11-24 — Enabled TailTray autostart

**Did:** Installed a user-session autostart desktop entry pointing at this project's
`.venv/bin/tailtray` launcher and verified that the launcher is executable.
**Why:** TailTray should be available automatically after each reboot/login.
**Next:** Confirm the icon appears after the next graphical login; no project code work
is pending.
**Notes:** The desktop-file validator reported only a non-blocking application-menu
category hint; it does not affect autostart.

## 2026-11-24 — Explain Tailscale write-permission failures

**Did:** Recognize `prefs write access denied` and other permission-denied responses,
then display the one-time `tailscale set --operator` recovery command instead of raw
daemon text. Added a unit test and installation guidance.
**Why:** The daemon allowed status reads but rejected menu actions, leaving an opaque
message at the point of use.
**Next:** Run the explicit operator setup as the desktop user, restart TailTray, and
retry a toggle.
**Notes:** The app remains deliberately unable to elevate itself or keep credentials.

## 2026-11-24 — Allow workspace transitions time to settle

**Did:** Increased the CLI timeout from 10 to 45 seconds and added an in-menu message
when a stopped profile disables workspace switching. Documented the start-first path for
returning from a stopped profile.
**Why:** `tailscale switch` waits for the selected profile's state transition, which can
take longer than a status or preference query; the former timeout could make a valid
switch appear broken.
**Next:** Retry Personal → Work after restarting TailTray. If Personal is stopped after
selection, choose Start Tailscale first.
**Notes:** This preserves the requested rule that workspace switching is unavailable
while the backend is stopped.

## 2026-11-24 — Stabilized state changes and stopped-state controls

**Did:** Captured checkbox values before asynchronous command dispatch, preventing a
rebuilt GTK menu from changing the value seen by the background action. Disabled
workspace, DNS, and route controls while Tailscale is stopped; added a test proving
the start action sends only `tailscale up`.
**Why:** The stop action could read a stale or rebuilt menu item, and configuration
controls should not be available against a stopped backend.
**Next:** Restart the app and verify that Stop transitions back to Start after refresh.
**Notes:** Checked DNS/routes values are existing per-profile preferences from
`tailscale debug prefs`; TailTray does not send them as part of `tailscale up`.

## 2026-11-24 — Matched preferences and profiles to the Tailscale CLI schema

**Did:** Changed preference discovery to `tailscale debug prefs`, which supplies
`CorpDNS` and `RouteAll`, and updated the workspace parser to use the CLI's lowercase
`id`, `nickname`, `tailnet`, `account`, and `selected` JSON fields. Profile picker rows
now use human-readable names instead of numeric IDs.
**Why:** Status JSON did not supply preferences, leaving their controls disabled, and
the switch parser did not recognize current profile-list field names.
**Next:** Relaunch TailTray and confirm that live preferences and profile labels appear.
**Notes:** The command contract was verified against Tailscale's current CLI source;
text-table fallback remains for clients that do not return JSON.

## 2026-11-24 — Clarified state actions and repaired workspace selection

**Did:** Made the running check item's label read `Start Tailscale` when stopped and
`Stop Tailscale` when running. Disabled workspace selection unless the backend is
running and replaced the invisible menu rebuild with a profile-picker dialog. Added a
fallback parser for the alpha command's text workspace list.
**Why:** The prior UI made the start/stop action ambiguous and did not visibly present
the profile list after it was fetched.
**Next:** Validate the picker against the local account list after Tailscale is running.
**Notes:** The JSON parser remains preferred; text parsing supports client versions that
return the human-readable workspace table despite the JSON request.

## 2026-11-24 — Added the Tailscale running toggle

**Did:** Added a `Tailscale running` menu toggle. Turning it on runs `tailscale up`;
turning it off runs `tailscale down`; both paths refresh state afterward. Added a unit
test for the exact command arguments and updated the user documentation and plan.
**Why:** The first UI could report a stopped backend but had no direct way to connect it.
**Next:** Launch on Linux Mint and verify the toggle against the local daemon.
**Notes:** The command still requires the existing Tailscale operator access arrangement.

## 2026-11-24 — Built the first TailTray application

**Did:** Added the Python package, safe Tailscale CLI client, GTK/Ayatana tray shell,
green/red SVG indicators, autostart desktop entry, installation guide, and five
standard-library unit tests. The client uses `status --json`, `switch --list --json`,
`switch <id>`, and the two requested `set` flags without shell invocation.
**Why:** Implemented the approved plan for local Tailscale status, workspace switching,
and DNS/route preference control.
**Next:** Install the Mint desktop bindings and conduct the live tray smoke test; set a
Tailscale operator only if the user wants password-free menu actions.
**Notes:** Tests and bytecode compilation pass. This workspace has no `gi` binding, and
the local daemon socket is unavailable to the current user, so neither condition was
changed during development.

## 2026-11-24 — Planned the Tailscale tray controller

**Did:** Reviewed the requested behavior and created `plan.md` for a Linux Mint tray
application: green/red status, workspace switching, DNS/routes toggles, safe CLI
execution, operator-access setup, tests, and installation.
**Why:** The template is now becoming a real local Tailscale controller and needs a
concrete, secure implementation path before code is added.
**Next:** Bootstrap the Python/AppIndicator shell and implement the Tailscale command
boundary in the plan's first two build steps.
**Notes:** Local Tailscale 1.104.7 exposes `status --json`, `switch --list --json`, and
the requested `set` flags; `switch` is alpha, so fixture-based parsing is planned.

## 2026-11-18 — Added the "gates protect operation, not the sandbox" principle

**Did:** Added a standing principle to `AGENTS.md` and logged decision #003: safety/
governance gates must be scoped to live operation, with an explicit no-gate lane for
sandboxed work on past/public/synthetic/non-personal data. Also deployed this kit into the
BalamSentry project (seeded its STATE/JOURNAL/DECISIONS/CHANGELOGs with real state).
**Why:** BalamSentry stalled on a self-imposed governance doc whose sign-off gated all
development — a catch-22 that recurs across projects. The principle makes future projects
inherit correct gate placement.
**Next:** Unchanged — use the kit on real projects; watch whether the new principle gets
applied when governance/hardening docs are written.
**Notes:** BalamSentry is the first real project to adopt this kit end to end.

## 2026-11-17 — Added README overview

**Did:** Added `README.md` as the top-level entry point: purpose of the template, a table
of all memory files and their roles, the session rhythm, and how to adopt it for a real
project. Logged paired changelog entries.
**Why:** The repo had no front-door document explaining what it is and how the pieces fit.
**Next:** Unchanged — use the kit on a real project.

## 2026-11-17 — Added shared agent instructions + dual changelog

**Did:** Added `AGENTS.md` as the single source of truth for the working workflow and
reduced `CLAUDE.md` to a pointer to it, so Claude, Codex, and any other engine follow the
same rules. Added a dual changelog: `CHANGELOG.md` (end-user, plain language, safe to
surface inside an app) and `CHANGELOG-DEV.md` (developer detail: request + change + why),
both append-only and paired by timestamp. Documented the "after every change" changelog
habit in AGENTS.md and logged decision #002.
**Why:** The maintainer frequently switches engines mid-day after hitting a usage limit;
one AGENTS.md avoids drift between per-engine instructions. The split changelog lets a
project ship release notes without leaking internal detail while keeping full technical
history.
**Next:** Use it on the first real project. The changelog habit is only as good as the
discipline of writing a paired entry after each change.
**Notes:** AGENTS.md is the emerging cross-agent convention; keeping CLAUDE.md as a thin
pointer means no second copy to maintain.

## 2026-10-31 — Established the resume kit

**Did:** Cleared out the old app-oriented baseline (standards docs, encoding scripts,
dual changelogs, build/deploy ship rules, git hooks) and replaced it with a minimal,
project-type-agnostic resume kit: `STATE.md`, `JOURNAL.md`, `DECISIONS.md`, and a short
`CLAUDE.md` explaining the read-on-start / update-on-end workflow.
**Why:** The previous baseline assumed every project was an app (referenced `make`, a
deploy target, a UI/API) which didn't fit non-app projects. The real goal is simpler:
help an AI pick up where we left off after weeks away, backed by a changelog memory.
**Next:** Use it. When a real project starts here, fill in STATE.md and log decisions.
**Notes:** Old scaffolding is recoverable from git history (commit before this one)
if any piece turns out to be worth keeping.
