# How to work in this project (any agent)

This file is the **single source of truth** for how an AI assistant — Claude, Codex,
or any other engine — should work in this repo. `CLAUDE.md` just points here, so the
rules stay identical no matter which engine you're using that day.

> **Why one file:** The maintainer often hits a usage limit on one engine mid-day and
> continues on another. Keeping the workflow in `AGENTS.md` (the cross-agent convention)
> means the handoff is seamless — the next engine picks up the same instructions and the
> same memory files, with no drift between two copies.

## The memory files

Five files carry the project's memory. Read the first three at the **start** of every
session; write to all of them (as relevant) at the **end**.

| File | What it holds | How it's written |
| --- | --- | --- |
| [STATE.md](STATE.md) | Where we left off *right now*: current focus, next steps, open questions, how to run things. | **Overwritten** to reflect the present. Always current, never a history. |
| [JOURNAL.md](JOURNAL.md) | What happened, newest first: one dated entry per working session. | **Append-only.** Never edit or delete past entries. |
| [DECISIONS.md](DECISIONS.md) | Durable "why we chose X" notes that outlive any one session. | Append a numbered entry when a real decision is made. |
| [CHANGELOG.md](CHANGELOG.md) | **End-user** summary of every change, newest first, timestamped. Safe to surface inside the app. | **Append-only**, one entry per change. Plain language, no jargon. |
| [CHANGELOG-DEV.md](CHANGELOG-DEV.md) | **Developer** detail for every change: the request, what changed, and why. | **Append-only**, one entry per change, paired with the user-facing one. |

## At the start of every session

1. Read [STATE.md](STATE.md) first — it's the single source of "what now".
2. Skim the top few entries of [JOURNAL.md](JOURNAL.md) for recent context.
3. Check [DECISIONS.md](DECISIONS.md) before changing anything architectural, so you
   don't reopen a settled choice (or do so knowingly).

## After every change (the changelog habit)

Whenever you make a meaningful change — a feature, a fix, a config or content change —
append **one paired entry** before moving on:

1. A line in [CHANGELOG.md](CHANGELOG.md): timestamp + a short, plain-language summary a
   non-technical end user would understand ("what's different for me").
2. A matching block in [CHANGELOG-DEV.md](CHANGELOG-DEV.md): same timestamp + the request
   that prompted it + what actually changed (files/approach) + why.

Keep the timestamps identical so the two files line up. Use the local date-time in
`YYYY-MM-DD HH:MM` form. Small, cosmetic, or purely internal tidy-ups don't need an entry
— use judgment; the changelog is for changes someone would care to know about.

## At the end of every session

1. **Rewrite [STATE.md](STATE.md)** so it describes the project as it stands now:
   what's done, what's next, what's unresolved. Delete anything no longer true.
2. **Prepend a new entry to [JOURNAL.md](JOURNAL.md)** (newest on top) using the template
   in that file: date, what changed, why, and anything the next session needs to know.
3. If a lasting decision was made, **add an entry to [DECISIONS.md](DECISIONS.md)**.
4. Make sure every change this session is reflected in the two changelogs.
5. Commit all of it together with the code so the memory and the work never drift apart.

## Principles

- STATE is the present, JOURNAL is the past, DECISIONS is the reasoning, the CHANGELOGs
  are the per-change record (one for users, one for developers). Keep them in their lanes.
- Write for a reader who has forgotten everything — because in a few weeks, they have.
- Prefer updating these files over writing new scattered notes. One place to look.
- This kit assumes nothing about the stack (no build tool, deploy target, or language
  baked in). Add project-specific conventions to this file as the project takes shape.
- **Gates protect operation, not the sandbox.** A safety, governance, security, or
  "best practice" gate exists to control what touches **real people, production, or the
  outside world** — not to block development itself. Scope every such gate to *live
  operation* (real data, real users, deploys, external action, anything irreversible),
  and explicitly leave a **no-gate lane for sandboxed work** on past, public, synthetic,
  or non-personal data that sends nothing and acts on nothing. A gate placed across
  development creates a catch-22: the working prototype that would justify the sign-off
  can't be built because the sign-off hasn't happened — a common, self-inflicted way for
  a project to stall. When you write a governance or hardening doc, state which lane each
  rule gates. Keep aspirational best-practices as *operation* gates; never let them
  become *build-time* requirements before there's anything to operate.
