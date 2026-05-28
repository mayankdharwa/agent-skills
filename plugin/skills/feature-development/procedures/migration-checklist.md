# MIGRATION-CHECKLIST lifecycle

Add or close items in `MIGRATION-CHECKLIST.md`. Tracks work owned by external teams or in other codebases.

## Modes

- **Add** — create a new item.
- **Close** — mark an existing item Done.

## Preconditions

- Feature dir is active.

`MIGRATION-CHECKLIST.md` may NOT exist yet — created lazily on the first item.

---

## Mode: Add

### Steps

1. **Lazy-create the file** if missing. See `reference/migration-checklist-shape.md` for the file-level structure and item shape. Initial file contents:
   ```markdown
   # Migration checklist

   Work owned by external teams or in other codebases. Grouped by owning team.
   ```

2. **Ask for the owning team**. The doc groups items by team via `##` headings. Examples: `## Voice`, `## Fabric`, `## Book`, `## Reach`, `## Access-Gateway`, `## Patient-Booking`.

3. **Determine item ID prefix from team name**. First letters of the team's `##` heading (typically one or two letters):
   - `Voice` → `V`
   - `Fabric` → `F`
   - `Book` → `B`
   - `Reach` → `R`
   - `Access-Gateway` → `AG`
   - `Patient-Booking` → `PB`

   If the prefix is ambiguous or could collide with another team in the same file, ask user. Numbering is per-team monotonic; each team's counter is independent (`V1, V2, ...` separate from `F1, F2, ...`).

4. **Ask for tag**. One of `Mandatory` / `Optional` / `Independent and Important` — see `reference/migration-checklist-shape.md` "Tags" for definitions.

5. **Ask for substantive content** (user-provided):
   - *Today* — current state.
   - *Change* — what changes (optionally split into Steps).
   - *Files affected* — list.
   - *Cutover dependency* — relationship to this project's cutover.
   - *Why <tag>* — for `Independent and Important`, justify why the owning project benefits regardless of this project. Skip for `Mandatory` / `Optional` unless the user wants to note it.

6. **Append the item** under the team's `##` heading. Format:
   ```markdown
   ### <Prefix><N> — <short title> [<tag>]

   **Today:** <text>

   **Change:**
   <text or steps>

   **Files affected:**
   - <file>
   - <file>

   **Cutover dependency:** <text>

   <**Why Independent and Important:** <text> — only if tag is "Independent and Important">

   **Status:** [ ] Pending
   ```

   If the team's `##` section doesn't exist yet, create it.

### Summary

Report: which ID was added under which team with which tag, and that status is Pending.

---

## Mode: Close

### Steps

1. **Identify the item** by ID (`<Prefix><N>`).

2. **Confirm closure** with user — what changed externally that lets us close this?

3. **Update the Status line**:
   ```
   **Status:** [x] Done — YYYY-MM-DD
   ```

   The item stays in the file as audit trail. Do NOT delete it.

4. **Check project-done gate** if this was a `Mandatory` item. After closing, check whether all `Mandatory` items are now closed:
   - If yes and top-level `PROGRESS.md` is all-`✅` and `OPEN-QUESTIONS.md` active index is empty → project is done. Surface to user and offer to route to `procedures/project-done-check.md`.

### Summary

Report: which ID closed, and the Mandatory-items-remaining count (or that all Mandatory items are closed).

---

## Errors

- Item ID collision (manual edit introduced a duplicate): surface and ask user to fix; do not silently renumber.
- Closing an already-closed item: surface and ask whether the user means to amend the date.
- Closing an item ID that doesn't exist: surface and list open items under that team's prefix.
- Tag is something other than the three valid values: surface and ask.

## Postconditions

**Add:** `MIGRATION-CHECKLIST.md` contains the new `### <Prefix><N>` heading under the right team's `##` section, with `<N>` one greater than any pre-existing item under that team's prefix. The `Status:` line reads `[ ] Pending`.

**Close:** the item's `Status:` line reads `[x] Done — YYYY-MM-DD`. The item itself remains in the file (closed items are audit trail, never deleted).
