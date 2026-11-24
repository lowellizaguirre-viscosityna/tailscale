# Decisions

> Durable "why we chose X" notes that outlive any single session. Append a numbered
> entry when a real decision is made; don't rewrite old ones. If a decision is later
> reversed, add a new entry that supersedes it (and say which number it replaces).

<!-- Template:

## NNN. Short title of the decision

**Date:** YYYY-MM-DD
**Decision:** what we decided.
**Why:** the reasoning and the main alternatives rejected.
**Status:** accepted | superseded by #NNN

-->

## 004. Use explicit Tailscale operator access for tray actions

**Date:** 2026-11-24
**Decision:** Plan the tray application around a one-time, user-approved
`tailscale set --operator=$USER` configuration, then invoke the Tailscale CLI with
argument arrays and no shell. If operator access is absent, leave actions disabled and
provide recovery guidance.
**Why:** The application needs routine local control without storing a password,
launching arbitrary commands through sudo, or creating a broad sudoers exception.
This uses Tailscale's documented local operator setting and keeps privilege delegation
explicit and scoped to Tailscale.
**Status:** accepted

## 001. Memory lives in three in-repo markdown files

**Date:** 2026-10-31
**Decision:** Track project continuity with `STATE.md` (present), `JOURNAL.md`
(append-only history), and `DECISIONS.md` (rationale), all plain markdown in the repo.
**Why:** The objective is resuming work after long gaps. Keeping it in-repo means the
memory travels with the code, lives in git history, works with any tool, and depends on
nothing external. Rejected: a heavy standards framework (over-fit to apps, the previous
baseline's failing) and relying on Claude's private memory dir (not portable, invisible
to humans and other tools).
**Status:** accepted

## 003. Gates protect operation, not the sandbox

**Date:** 2026-11-18
**Decision:** Add a standing principle to `AGENTS.md`: safety/governance/security/"best
practice" gates must be scoped to *live operation* (real people, production, external
action, irreversible steps), with an explicit no-gate lane for sandboxed work on past,
public, synthetic, or non-personal data that sends and acts on nothing. Governance and
hardening docs should state which lane each rule gates.
**Why:** Surfaced by the BalamSentry project, which stalled on a self-imposed governance
doc whose sign-off gated *all development* — including building the prototype needed to
justify the sign-off. That catch-22 is a recurring, self-inflicted failure mode across
the maintainer's many projects. Baking the rule into the kit makes future projects
inherit correct gate placement by default. Rejected: treating it as a one-off fix in
BalamSentry only (it would recur elsewhere).
**Status:** accepted

## 002. One AGENTS.md for all engines, plus a dual changelog

**Date:** 2026-11-17
**Decision:** Put the working workflow in `AGENTS.md` (the cross-agent convention) as the
single source of truth, and make `CLAUDE.md` a thin pointer to it. Add two append-only,
newest-first changelogs written after every change: `CHANGELOG.md` (end-user, plain,
app-surfaceable) and `CHANGELOG-DEV.md` (developer: request + change + why), paired by an
identical timestamp.
**Why:** The maintainer often switches engines mid-day after hitting a usage limit; a
single AGENTS.md makes handoffs seamless and avoids drift between duplicated per-engine
instruction files. Rejected: maintaining separate full instructions in CLAUDE.md and a
Codex file (they would diverge). Splitting the changelog keeps shippable release notes
free of internal detail while preserving full technical history alongside.
**Status:** accepted
