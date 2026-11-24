# How to work in this project

> **The workflow for this repo lives in [AGENTS.md](AGENTS.md).** It's the single source
> of truth, shared by every engine (Claude, Codex, and others), so the rules never drift
> between copies. Read it now.

In short, so you're not flying blind if you only read this file:

- **Start of session:** read [STATE.md](STATE.md), skim [JOURNAL.md](JOURNAL.md), check
  [DECISIONS.md](DECISIONS.md).
- **After every change:** append a paired entry to [CHANGELOG.md](CHANGELOG.md)
  (end-user, plain) and [CHANGELOG-DEV.md](CHANGELOG-DEV.md) (developer detail), with the
  same timestamp.
- **End of session:** rewrite [STATE.md](STATE.md), prepend to [JOURNAL.md](JOURNAL.md),
  add to [DECISIONS.md](DECISIONS.md) if a lasting decision was made, and commit it all
  with the code.

See [AGENTS.md](AGENTS.md) for the full version of each of these.
