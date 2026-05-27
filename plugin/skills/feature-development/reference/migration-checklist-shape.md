# Migration checklist shape

Read when adding or closing a `MIGRATION-CHECKLIST.md` item.

## File-level structure

- H1: `# Migration checklist`
- Items grouped by owning team under `##` headings (e.g., `## Voice`, `## Fabric`).
- Items are `###` subheadings within each team section.

## Item ID

`<TeamPrefix><N>` where prefix is the first letters of the team's `##` heading; `<N>` is per-team monotonic (see `reference/sequence-rules.md`).

## Tags

One per item, in `[brackets]` in the heading:

- **Mandatory** — must be done before project go-live. Blocks cutover.
- **Optional** — can be done later; does not block.
- **Independent and Important** — work stands on its own merit; other projects benefit; does not gate this project.

## Item shape

```
### <Prefix><N> — <short title> [<Mandatory | Optional | Independent and Important>]

**Today:** <current state>

**Change:**
<text or bulleted steps>

**Files affected:**
- <file>
- <file>

**Cutover dependency:** <text>

**Why Independent and Important:** <only if tag is Independent and Important>

**Status:** [ ] Pending
```

## Closed items

`**Status:** [x] Done — YYYY-MM-DD`. Closed items remain in the file forever as audit trail; never delete.

## Project-done gate

Every `Mandatory` item closed. `Independent and Important` and `Optional` items do not gate; the file may live on with the feature dir.
