# DECISIONS lift criteria

Read when scanning callouts or `decision:` tags for promotion to `DECISIONS.md`. Same rubric for topic-lock sweep, section-archive sweep, and surgical-reopen lift.

## The three criteria

All three must be true for a decision to be lifted:

1. **Hard to reverse** — reversing it would touch multiple unrelated files or phases.
2. **Surprising without context** — a future reader will ask "why did they do it this way?" without the rationale.
3. **Real trade-off** — there were genuine alternatives and one was picked for specific reasons.

If any of the three is missing, leave the decision inline as a `Review comment` callout (exploration) or `decision:` tag (build).

Expect roughly 10–20% of callouts / tags to qualify.

## Sweep cadences

- **Topic-lock** — scan the topic's `*-EXPLORATION.md` `Review comment` callouts before archiving topic `PROGRESS.md`. For the `custom` topic, the sweep walks all `.md` files inside each `exploration/custom/<sub-exploration>/` folder (excluding `INDEX.md`, `PROGRESS.md`, and any nested `_archive/`) — see `procedures/custom.md` and `reference/custom-shape.md`.
- **Section-archive** — scan `build/code-review/<section>.md` `decision:` tags before archiving.
- **Immediate lift** — at any time within a topic or section, when a decision is obviously course-altering. The inline callout / tag stays in place with a backlink as normal; the entry lands in `DECISIONS.md` straight away. Immediate-lifted decisions are skipped during the topic-lock or section-archive sweep (check `DECISIONS.md` `Source:` lines for pre-existing entries).

## Lift mechanics

The inline `Review comment` callout (or `decision:` tag) **stays in the source doc** — it carries the full context. The `DECISIONS.md` entry carries the distilled "decision + why" plus a backlink to the source. One-way pointer: `DECISIONS.md` → inline. The central file is greppable; the inline file is readable.

Numbering: per-feature monotonic `#N` for entries in feature-level `DECISIONS.md`. Repo-root `docs/DECISIONS.md` has its own independent counter (see `procedures/cross-feature-lift.md`).

## Cross-feature scope

After lifting, check whether the decision crosses features. See `procedures/cross-feature-lift.md`.
