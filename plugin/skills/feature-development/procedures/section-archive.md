# Section-archive (build phase)

Close a build section when every item in its `code-review/<section>.md` is tagged. Triggers a DECISIONS sweep on `decision:` tags, then archives the file.

## Preconditions

- Build phase is active (`build/` exists; `build/PROGRESS.md` shows the section row).
- `build/code-review/<section>.md` exists with at least one item.
- Every item carries one of the four tags: `fixed`, `wont-fix: <reason>`, `decision: <text>`, `spec-changed: <link>`.

If any item is untagged, surface and refuse to archive — user must tag first.

Lift criteria + immediate-lift mechanics: `reference/lift-criteria.md`.

## Steps

### 1. Verify all items tagged

Read `build/code-review/<section>.md`. Check every item. If any are untagged, surface the list of untagged items and remind the user that each must carry one of: `fixed` / `wont-fix: <reason>` / `decision: <text>` / `spec-changed: <link>`. Stop. Do not proceed.

### 2. DECISIONS sweep on `decision:` tags

Enumerate items tagged `decision: ...`. Skip any already lifted via immediate-lift (check `DECISIONS.md` `Source:` lines). For each remaining, apply the three lift criteria from `reference/lift-criteria.md`.

> Item: "`<one-line summary of the item>`"
> Decision tag: "`<decision text>`"
> - Hard-to-reverse: Y / N
> - Surprising: Y / N
> - Real-trade-off: Y / N
> Recommend: **LIFT to DECISIONS.md #N | LEAVE inline**.
> Confirm / flip / re-discuss?

For confirmed LIFTs: append entry to `DECISIONS.md` (next monotonic `#N`) with backlink to the source code-review item (file + item identifier).

Cross-feature check: if the decision affects code outside this feature, route to `procedures/cross-feature-lift.md`.

### 3. Archive the file

Determine archive filename:
- Path: `build/_archive/code-review/<section>_<YYYY-MM-DD>_<seq>.md`
- `<seq>` per `reference/sequence-rules.md` (per-section monotonic across time).

Move: `git mv build/code-review/<section>.md build/_archive/code-review/<section>_<YYYY-MM-DD>_<seq>.md`.

The live file is removed — `ls build/code-review/` then shows only sections with open items.

### 4. `build/testing/<section>.md` stays in place

Do NOT archive or move the testing file. It's permanent reference material once code exists.

### 5. Update `build/PROGRESS.md`

Section rows carry dual test+code status (see `templates/progress-build.md`). On section close, flip the section's row icon to `✅` AND set both `tests: ✅` and `code: ✅` in the row's trailing status block. During the section's life, tests and code may move independently.

Update `## Current focus`:
- If there's a next `⏳` section: name it.
- If every section is `✅`: this is build phase-lock. Set narrative to:
  > Build locked. All sections ✅ — archiving build/PROGRESS.md.

  Then archive `build/PROGRESS.md` (path: `build/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md`, per-directory monotonic across time — counter does not reset per day).

  Update top-level `PROGRESS.md`: `🚧 build → ✅`.

### 6. Summarise

Report: section archived to its destination path, sweep results (count of `decision:` tags considered and how many lifted to DECISIONS.md), that `build/testing/<section>.md` stays in place, and whether build phase-lock is triggered or which sections remain.

## Post-archive findings

If new findings surface for this section after archive, **create a new** `build/code-review/<section>.md` (do NOT edit the archive). When that new file closes, archive with the next per-section sequence number. The new file is independent; cross-references happen via git history if needed.

## Errors

- Untagged items present: surface, stop.
- Sequence number collision (shouldn't happen with correct read-then-write): surface and ask.
- Section name doesn't match any `code-review/*.md`: drift — surface and ask.
- Section row missing from `build/PROGRESS.md`: drift — surface and ask whether to add the row or whether the section name is wrong.

## Postconditions

- `build/code-review/<section>.md` no longer exists at the live path.
- `build/_archive/code-review/<section>_<YYYY-MM-DD>_<seq>.md` exists with `<seq>` one greater than any pre-existing archive of THIS section.
- `build/testing/<section>.md` is untouched.
- The section's row in `build/PROGRESS.md` shows `✅` with both `tests: ✅` and `code: ✅` in its dual-status block.
- For each confirmed lift: `DECISIONS.md` has a new entry whose `Source:` backlinks to the code-review item.
