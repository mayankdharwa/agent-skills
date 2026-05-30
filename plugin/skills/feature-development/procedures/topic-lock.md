# Topic-lock

Lock an entire exploration topic. Triggered when every non-deferred row in the topic `PROGRESS.md` is `✅`. Runs a DECISIONS sweep on the topic's `Review comment` callouts, then archives the topic `PROGRESS.md`. Applies to all five topics — the four standard topics (`schema`, `apis`, `jobs`, `code-structure`) and `custom` if it exists.

## Preconditions

- Every `🚧` row in the topic `PROGRESS.md` has flipped to `✅`.
- Any `⏳ ... — deferred:` rows have either been resolved this pass (becoming `✅`) or are about to be escalated as scope change.

Lift criteria + immediate-lift mechanics: `reference/lift-criteria.md`.

## Steps

### 1. Loop-back to deferred rows (if any)

If the topic has any `⏳ ... — deferred:` rows:

For each, check whether the deferral reason has resolved:
- Offline-resolves path: read `OPEN-QUESTIONS.md`. Did the blocking Q<N> get resolved? If yes, surface its resolution and ask the user to lock the unit normally (route to `procedures/unit-lock.md`). If no, surface as still-blocked.
- Research path: read the referenced `references/<file>.md`. Was it written? If yes, surface and ask user to lock. If no, surface as awaiting reference.

If unresolved deferrals remain, surface the list and ask the user to pick one of two paths: **continue waiting** (leave the topic open until deferral resolves) or **scope change** (drop the unit from the topic; record via a Review comment and consider for DECISIONS.md).

If user picks "continue waiting", stop. The topic cannot lock yet.

If user picks "scope change", route to a mini scope-change flow:
- Ask for a Review comment text justifying the scope drop.
- Append the callout to the exploration doc with next monotonic number.
- Remove the row from the `## Progress` table.
- Continue with the sweep.

### 2. DECISIONS sweep (judgment, walks user through)

Read the topic's `*-EXPLORATION.md` file(s). For the `custom` topic, walk `exploration/custom/**/*.md` and exclude `exploration/custom/INDEX.md`, `exploration/custom/PROGRESS.md`, and anything inside any `_archive/` directory (including nested archives a user may maintain inside a sub-exploration folder). Enumerate every `Review comment #N` callout across the read files. Skip any callout whose decision has already been lifted to `DECISIONS.md` via immediate-lift (check `DECISIONS.md` `Source:` lines).

For each remaining callout, apply the three lift criteria from `reference/lift-criteria.md`.

Surface each callout to the user with your pre-judgment:

> Callout #<N> (`<unit>`): "`<decision summary>`"
> - Hard-to-reverse: Y / N
> - Surprising: Y / N
> - Real-trade-off: Y / N
> Recommend: **<LIFT to DECISIONS.md #M with title "<auto-drafted title>"> | <LEAVE inline>**.
> Confirm / flip / re-discuss?

The user answers per callout: `confirm` (apply skill's recommendation), `flip` (do the opposite), or `re-discuss` (skip for now; the callout stays inline but no entry written).

For confirmed LIFTs: append a new entry to `DECISIONS.md` using the canonical shape in `templates/decisions.md`. Determine `#M` per `reference/sequence-rules.md` (per-feature monotonic). `Source:` is a link to the inline `Review comment` callout in the exploration doc.

The inline callout stays untouched in the exploration doc — do NOT delete or rewrite it.

### 3. Check for cross-feature scope

For each lifted decision, ask whether it affects code or conventions outside this feature. If yes, route the lifted entry to `procedures/cross-feature-lift.md`.

### 4. Archive the topic `PROGRESS.md`

Determine the archive filename:
- Path: `exploration/<topic>/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md`
- `<seq>` per `reference/sequence-rules.md` (per-directory monotonic across time).

Move the file: `git mv exploration/<topic>/PROGRESS.md exploration/<topic>/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md`.

(If not a git repo, use `mv`.)

Confirm via `ls exploration/<topic>/` — `PROGRESS.md` is no longer at the live path.

### 5. Update top-level `PROGRESS.md`

Remove the pointer line for this topic. If other topic pointers remain under the `🚧 exploration` row, leave the row as is. The `🚧 exploration` row stays `🚧` until every live topic locks.

Check whether all live exploration topics are now locked — the four standard topics plus `custom` if `exploration/custom/` exists. A topic is locked when its `PROGRESS.md` lives only in `_archive/`. Run `ls docs/<feature>/exploration/` to enumerate; check each.

If yes: route to `procedures/distill.md` for one-pass spec distillation.

### 6. Summarise

Report: topic locked; sweep result (callouts considered and how many lifted, with entry numbers); archive path of the topic `PROGRESS.md`; whether exploration phase-lock is triggered or which topics remain open.

## Errors

- A row is `🚧` (not `✅`) at sweep time: surface, refuse to sweep — user must lock it first.
- An exploration doc was hand-edited and `Review comment` numbers are non-monotonic: surface and ask the user to fix; do not silently renumber.
- Archive sequence number collision (shouldn't happen with correct read-then-write): surface and ask.

## Postconditions

- `exploration/<topic>/PROGRESS.md` no longer exists at the live path.
- `exploration/<topic>/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md` exists with `<seq>` one greater than any pre-existing archive in that directory.
- The topic's pointer line is gone from top-level `PROGRESS.md`.
- `DECISIONS.md` contains entries for each confirmed-lifted callout, each carrying a `Source:` line that backlinks to the inline `Review comment`.
- The inline `Review comment` callouts remain in the exploration doc (none deleted).
