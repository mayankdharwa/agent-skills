# TECH-DEBT lifecycle

Add or close items in `TECH-DEBT.md`. Tracks own-codebase, non-blocking code-quality follow-ups discovered during build or review — refactor opportunities, naming inconsistencies, util extractions, "do it this way not that way" observations. **Not bugs** (tests don't catch these), and **not external work** (that's `MIGRATION-CHECKLIST.md`).

`TECH-DEBT.md` is standalone — it is **not** part of the code-review finding cycle. A Review Agent finding never resolves to a TD entry; review findings resolve only via `fixed` / `wont-fix:` / `decision:` / `spec-changed:` as today.

## How items get added

User-invoked. The user explicitly asks to log a TD item.

Agents may **propose** candidates — the Coding Agent (while writing or reading code) and the Review Agent (while reading code, outside the finding cycle) may surface "this looks like a TD candidate" with a one-line summary. The user accepts or declines.

A Review-Agent TD candidate is a **conversational suggestion only**. It is never written into `build/code-review/<section>.md`, never tagged as a finding resolution, and never causes a file edit on its own. If the user accepts, the user (not the Review Agent) invokes Add mode below. Agents do not silently append.

## Modes

- **Add** — create a new item.
- **Close** — mark an existing item Done.

## Preconditions

- Feature dir is active.

`TECH-DEBT.md` may NOT exist yet — created lazily on the first item.

---

## Mode: Add

### Steps

1. **Lazy-create the file** if missing. See `reference/tech-debt-shape.md` for the file-level structure and item shape. Initial file contents:
   ```markdown
   # Tech debt

   Own-codebase code-quality follow-ups deferred from the current pass. Flat monotonic IDs (`TD1`, `TD2`, ...). Non-blocking; revisit on a later sweep.
   ```

2. **Determine next ID**. Scan the file (both open and closed items) for the highest `TD<N>`; new ID is `N+1`. If empty, start at `TD1`. Per-feature monotonic; numbers never reuse, even after close.

3. **Confirm substantive content** with the user (the agent may have proposed a draft; the user approves or amends):
   - *Today* — how the code currently looks / what's awkward.
   - *Proposed change* — what should change. Direction, not a binding implementation.
   - *Files affected* — list.
   - *Why deferred* — out of scope for this pass, risk, dependency, time, etc.

4. **Append the item** at the bottom of the file, after any existing items. Format:
   ```markdown
   ### TD<N> — <short title>

   **Today:** <text>

   **Proposed change:** <text>

   **Files affected:**
   - <file>
   - <file>

   **Why deferred:** <text>

   **Status:** [ ] Pending
   ```

### Summary

Report: which `TD<N>` was added.

---

## Mode: Close

### Steps

1. **Identify the item** by ID (`TD<N>`).

2. **Confirm closure** with user — what changed that lets us close this? Typically a commit / PR ref.

3. **Update the Status line**:
   ```
   **Status:** [x] Done — YYYY-MM-DD
   ```

   Optionally append `— see <commit/PR ref>` if the user provides one. The item stays in the file as audit trail. Do NOT delete it.

### Summary

Report: which `TD<N>` closed.

---

## Errors

- Item ID collision (manual edit introduced a duplicate): surface and ask user to fix; do not silently renumber.
- Closing an already-closed item: surface and ask whether the user means to amend the date.
- Closing a `TD<N>` that doesn't exist: surface and list open items.

## Postconditions

**Add:** `TECH-DEBT.md` contains the new `### TD<N>` heading at the bottom of the file, with `<N>` one greater than any pre-existing item (open or closed). The `Status:` line reads `[ ] Pending`.

**Close:** the item's `Status:` line reads `[x] Done — YYYY-MM-DD` (optionally with a commit/PR ref). The item itself remains in the file (closed items are audit trail, never deleted).

## Project-done relationship

Non-blocking — see `reference/tech-debt-shape.md` "Project-done gate" for the rule, and `procedures/project-done-check.md` step 5 for how the heads-up is produced.
