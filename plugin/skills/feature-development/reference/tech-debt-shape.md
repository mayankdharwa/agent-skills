# Tech debt shape

Read when adding or closing a `TECH-DEBT.md` item.

## File-level structure

- H1: `# Tech debt`
- No grouping. Items are `###` subheadings, listed in monotonic order by ID.
- Closed items remain in place (in their original order) as audit trail.

## Item ID

`TD<N>` where `<N>` is per-feature monotonic across the whole file. New items take `max(existing) + 1`. Numbers never reuse, even after close. See `reference/sequence-rules.md`.

## Item shape

```
### TD<N> — <short title>

**Today:** <how the code currently looks / what's awkward>

**Proposed change:** <what should change — direction, not a binding implementation>

**Files affected:**
- <file>
- <file>

**Why deferred:** <out of scope for this pass, risk, dependency, time, etc.>

**Status:** [ ] Pending
```

## Closed items

`**Status:** [x] Done — YYYY-MM-DD` (optionally `— see <commit/PR ref>`). Closed items remain in the file forever as audit trail; never delete.

## Project-done gate

`TECH-DEBT.md` items do not gate project-done. Open items are surfaced as a heads-up count during `procedures/project-done-check.md` but never block. The file may live on with the feature dir indefinitely.

## What does NOT belong here

- **Bugs** — failures that tests should catch. Fix in-band or log via code-review findings.
- **External work** — anything owned by another team / codebase. Goes in `MIGRATION-CHECKLIST.md`.
- **Open questions** — anything needing user input on the spec. Goes in `OPEN-QUESTIONS.md`.
- **Locked-spec changes** — route through `procedures/surgical-reopen.md`.
- **Active code-review findings** — review findings stay in `build/code-review/<section>.md` and resolve only via `fixed` / `wont-fix:` / `decision:` / `spec-changed:`. TECH-DEBT is not a resolution path for findings.
