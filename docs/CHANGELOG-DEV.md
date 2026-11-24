# Developer Changelog

> **Developer** changelog: the detailed, technical record of every change, newest first.
> Each entry pairs with a line in the end-user [CHANGELOG.md](CHANGELOG.md) via an
> identical timestamp. Capture the request that prompted the change, what actually
> changed, and why — enough that a future developer (or a different AI engine) can
> reconstruct the reasoning. **Append-only**; never edit past entries.

<!-- Add new entries to the TOP:

## YYYY-MM-DD HH:MM — Short title

**Request:** what was asked for (quote or paraphrase the prompt).
**Changed:** files touched, approach taken, anything notable.
**Why:** the reasoning; alternatives considered or rejected.

-->

## 2026-11-24 14:15 — Install an on-demand TailTray desktop entry

**Request:** Add a desktop file that can launch TailTray on demand.
**Changed:** Installed and validated
`/home/lowell/.local/share/applications/tailtray.desktop`, with absolute executable and
icon paths matching the project virtual environment.
**Why:** Linux Mint discovers per-user applications from this XDG directory; it is
separate from the autostart entry so the user can launch the application manually.

## 2026-11-24 14:00 — Register TailTray for user-session autostart

**Request:** Start the working TailTray application automatically after every reboot.
**Changed:** Installed `/home/lowell/.config/autostart/tailtray.desktop`, pointing
`Exec` at `/media/lowell/storage/github/tailscale/.venv/bin/tailtray` and `Icon` at the
project SVG; verified the file and executable.
**Why:** A per-user XDG autostart entry is the appropriate Linux Mint mechanism and does
not require a system-wide service or administrator privileges.

## 2026-11-24 13:45 — Make prefs-write denial actionable

**Request:** TailTray displayed `prefs write access denied` while attempting a toggle.
**Changed:** Map daemon permission failures to the documented one-time operator setup,
add a focused unit test, and update user/project documentation.
**Why:** The raw local-API error does not tell the desktop user how to grant the scoped
Tailscale permission needed for write actions.

## 2026-11-24 13:30 — Extend workspace-switch timeout

**Request:** Switching from Work to Personal succeeded, but switching back no longer
worked.
**Changed:** Increased the shared Tailscale command timeout to 45 seconds and added
stopped-profile guidance to the tray menu and documentation.
**Why:** `tailscale switch` blocks while the target profile transitions; a 10-second
timeout was too short for an account/profile switch on some connections. The UI retains
the requested stopped-state disablement, with clear recovery instructions.

## 2026-11-24 13:15 — Snapshot toggle state and disable stopped configuration

**Request:** Stop did not reliably change the displayed state; configuration should be
disabled when stopped; clarify whether initially checked preferences were sent at start.
**Changed:** Snapshot GTK check-menu values before background dispatch, gate workspace,
DNS, and routes on `Running`, add a command test proving Start calls only `tailscale
up`, and document the preference semantics.
**Why:** The old lambdas read widget state after menu reconstruction, which could race.
Preferences are observed from persistent Tailscale state, not implicitly applied by the
start action.

## 2026-11-24 13:00 — Match current preference and profile schemas

**Request:** DNS/routes controls remained disabled while running, and workspace picker
rows showed integer values rather than profile names.
**Changed:** Read `CorpDNS` and `RouteAll` from `tailscale debug prefs`; parsed the
documented lowercase profile JSON fields and rendered nickname, account, and tailnet;
updated tests and user documentation.
**Why:** `status --json` is not the source of editable preferences, while `switch --list
--json` has a different field shape than the original generic parser expected.

## 2026-11-24 12:45 — Repair workspace picker and state labels

**Request:** Label the state control as Start or Stop based on status, disable workspace
switching while stopped, and make the available workspace list visible.
**Changed:** Replaced the generic running label with state-specific labels; gated the
workspace item on `Running`; displayed fetched profiles in a radio-button dialog; and
added a text-table parsing fallback plus test for alpha `switch --list` output.
**Why:** Rebuilding the tray menu after an asynchronous profile fetch did not show the
selection result to the user, and the state control label did not describe its action.

## 2026-11-24 12:30 — Add Tailscale running control

**Request:** Add a visible control to run `tailscale up` because the tray app only
reported a stopped state.
**Changed:** Added `TailscaleClient.set_running`, a checkable `Tailscale running` menu
item wired to `tailscale up`/`tailscale down`, a command-level unit test, and matching
documentation/state records.
**Why:** Status visibility alone did not let the user recover a stopped Tailscale
connection from the application.

## 2026-11-24 12:15 — Implement TailTray

**Request:** Build the application described by the approved `plan.md`.
**Changed:** Added the `tailtray` Python package, shell-free subprocess client,
GTK/Ayatana indicator UI, red/green SVG assets, desktop launcher, Linux Mint setup
guide, and five unit tests. Updated the current project state and session/changelog
records.
**Why:** This implements the requested local status indicator, workspace switching, and
DNS/routes toggles while keeping routine privilege delegation explicit and avoiding
password handling or broad sudo configuration.

## 2026-11-24 12:00 — Plan the Tailscale tray controller

**Request:** Review `instructions.md` and create a plan for the requested simple
Tailscale tray application.
**Changed:** Added `plan.md` with the Linux Mint/Python/AppIndicator architecture,
validated local Tailscale 1.104.7 command contract, dynamic menu behavior, testing,
autostart, and acceptance checks. Updated project state and added decision #004 plus
paired changelog and journal entries.
**Why:** The app needs a secure answer to its current sudo requirement before UI work
begins. The plan scopes access through Tailscale's explicit operator setting and keeps
all subprocess execution shell-free.

## 2026-11-18 15:30 — Add "gates protect operation, not the sandbox" principle

**Request:** Capture, as a short principle in the kit, the lesson from BalamSentry: a
governance/safety gate should protect operation on real people and production, never the
sandbox; a gate across development self-locks the project.
**Changed:** Added a bullet to the Principles section of `AGENTS.md` defining the rule —
scope gates to live operation, leave a no-gate lane for past/public/synthetic/non-personal
sandbox work, and state which lane each rule gates in any governance/hardening doc. Logged
decision #003 and paired changelog entries.
**Why:** The catch-22 that stalled BalamSentry (sign-off gating the prototype that would
justify the sign-off) is a recurring, self-inflicted failure mode. Putting the rule in the
cross-engine source of truth makes every future project inherit correct gate placement.

## 2026-11-17 12:20 — Add README describing the base project

**Request:** Add a README.md describing the purpose of this base project.
**Changed:** Created `README.md` — explains the resume-kit purpose, a table of all the
memory files and their roles, the start/after-change/end-of-session rhythm, and how to
adopt the template for a real project. Added paired changelog entries.
**Why:** The repo had no top-level entry point; a README is the conventional first thing a
visitor (human or AI) reads, and it ties the file set together at a glance.

## 2026-11-17 12:00 — Add shared agent instructions + dual changelog to the resume kit

**Request:** Maintainer wanted (1) a separate markdown for Codex / other agents, since
they frequently switch engines after hitting a usage limit, and (2) a dual-changelog
system — an end-user summary and a developer summary, each timestamped, written after
every change, with the end-user one optionally includable in the application.

**Changed:**
- Added `AGENTS.md` as the single source of truth for the working workflow (cross-agent
  convention read by Codex and others).
- Rewrote `CLAUDE.md` into a thin pointer to `AGENTS.md` plus a short summary, so the two
  engines never follow divergent rules.
- Added `CHANGELOG.md` (end-user, plain language, app-surfaceable) and this
  `CHANGELOG-DEV.md` (developer detail), both append-only and newest-first, paired by
  timestamp.
- Documented the "after every change" changelog habit and the five memory files in
  `AGENTS.md`.

**Why:** A single `AGENTS.md` avoids drift between duplicated per-engine instructions and
makes mid-day engine handoffs seamless. Splitting the changelog into user- and
developer-facing files lets the project ship release notes from `CHANGELOG.md` without
leaking internal detail, while preserving full technical history alongside it.
