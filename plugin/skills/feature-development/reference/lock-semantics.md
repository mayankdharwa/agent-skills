# Lock semantics

Locks are closure actions. Three scopes:

| Scope | What it means | What it triggers |
|---|---|---|
| **Unit lock** (exploration) / **per-reference lock** (references) / **section lock** (build) | One table / endpoint / job / class (exploration), one reference file, or one build section is finalised. Triggered by user confirmation. | A numbered `Review comment` callout appended (exploration). The unit's row marked `✅` in its `PROGRESS.md`. For build: section's `code-review/<section>.md` fully tagged → archived. |
| **Topic lock** (exploration only) | Every unit in the topic is unit-locked. Applies to the four standard topics and to `custom` if it exists. | Topic's `PROGRESS.md` archives. Spec is NOT written yet. Triggers a DECISIONS sweep of the topic's `Review comment` callouts (for `custom`, sweep walks all sub-exploration `.md` files). |
| **Phase lock** | Every live topic (exploration) or every section (build) is locked. Exploration phase-lock requires the four standard topics plus `custom` if `exploration/custom/` exists. | For exploration phase-lock: one-pass spec distillation across the four standard spec files plus any extra files generated from `custom` fold targets. For build phase-lock: `build/PROGRESS.md` archives. |

`spec/` is the *output* of exploration phase-lock; it has no lock action of its own.

Locks are reversed only via surgical reopen (`procedures/surgical-reopen.md`). Outside that flow, a locked decision is immutable.

## Phase termination gates

- **Topic-lock**: every unit row `✅`. Sweep `Review comment` callouts; archive topic `PROGRESS.md`; remove topic pointer from top-level.
- **Exploration phase-lock**: every live topic locked — the four standard topics plus `custom` if it exists. One-pass distillation across `spec/{SCHEMA,APIS,JOBS,CODE-FILES}.md` plus any extra files generated from `custom` fold targets (see `reference/custom-shape.md`). Top-level `exploration` → `✅`; `spec` jumps straight from `⏳` → `✅` (no `🚧`).
- **Section-archive** (build): every item tagged. Sweep `decision:` tags; archive `code-review/<section>.md`. `testing/<section>.md` stays in place.
- **Build phase-lock**: every section `✅`. Archive `build/PROGRESS.md`. Top-level `build` → `✅`.
- **Project-done**: top-level `PROGRESS.md` all-`✅` + `OPEN-QUESTIONS.md` active index empty + every `Mandatory` migration item closed. See `procedures/project-done-check.md`.

## Top-level `PROGRESS.md` update cadence

Touched only on lock-scope transitions:

1. **Phase begins** (first topic / section starts) — flip the phase line from `⏳` to `🚧`; add a pointer to the active topic's / section's `PROGRESS.md`.
2. **Topic / section locks** — remove its pointer from under the phase line.
3. **Last topic / section in a phase locks** — flip the phase line from `🚧` to `✅`.
4. **Surgical reopen begins** (`procedures/surgical-reopen.md`) — if a previously locked phase row is `✅`, flip it back to `🚧` and add a pointer to the resurrected topic `PROGRESS.md`. On reopen close, treat as triggers 2–3: remove the pointer; flip back to `✅` if no other live topic `PROGRESS.md` remains.

No other edits. Top-level `PROGRESS.md` lists only *active* topics under a `🚧` phase row; locked topics' pointers are removed at lock-time.
