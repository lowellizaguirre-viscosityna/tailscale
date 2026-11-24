# Base Project — a resumable starting point

A minimal, stack-agnostic template whose one job is to make a project **easy to pick back
up after a long gap**. Clone or fork it to start something new, and the memory scaffolding
is already in place — so weeks later you (or an AI assistant on any engine) can resume
without re-reading everything.

## Why this exists

Projects get set down and picked up days or weeks apart. By then the context is gone: what
was in progress, why a thing was built the way it was, how to run it. This template keeps
that context in a few plain-markdown files that travel with the code, live in git history,
and depend on no external tool or service.

## The files

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | **Single source of truth** for how to work in the repo. Read by every engine (Claude, Codex, others). |
| [CLAUDE.md](CLAUDE.md) | Thin pointer to AGENTS.md so Claude and other engines follow identical rules. |
| [STATE.md](STATE.md) | The present: current focus, next steps, open questions, how to run things. Overwritten to stay true *now*. |
| [JOURNAL.md](JOURNAL.md) | Append-only history, newest first — one entry per working session. |
| [DECISIONS.md](DECISIONS.md) | Durable "why we chose X" notes that outlive any one session. |
| [CHANGELOG.md](CHANGELOG.md) | End-user changelog, plain language, timestamped. Safe to surface inside an app. |
| [CHANGELOG-DEV.md](CHANGELOG-DEV.md) | Developer changelog: the request, what changed, and why. Paired to the user entry by timestamp. |

## The rhythm

- **Start of a session:** read [STATE.md](STATE.md), skim [JOURNAL.md](JOURNAL.md), check
  [DECISIONS.md](DECISIONS.md).
- **After every change:** append a paired entry to [CHANGELOG.md](CHANGELOG.md) (end-user)
  and [CHANGELOG-DEV.md](CHANGELOG-DEV.md) (developer), with the same timestamp.
- **End of a session:** rewrite [STATE.md](STATE.md), prepend to [JOURNAL.md](JOURNAL.md),
  log any lasting decision in [DECISIONS.md](DECISIONS.md), and commit it all with the code
  so the memory and the work never drift apart.

See [AGENTS.md](AGENTS.md) for the full workflow.

## Using it for a real project

1. Fill in "What this project is" in [STATE.md](STATE.md).
2. Record your first real decision (stack, structure) in [DECISIONS.md](DECISIONS.md).
3. Keep the rhythm above as the project grows. Add project-specific conventions to
   [AGENTS.md](AGENTS.md).
