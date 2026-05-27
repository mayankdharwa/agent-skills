# Decisions

<!--
Canonical entry shape — authoritative. Every procedure that appends a DECISIONS entry
(topic-lock, section-archive, surgical-reopen, cross-feature-lift) uses this shape verbatim.

## #N — <short title>

*Lifted: YYYY-MM-DD · Source: [<path>/<file> §X Review comment #M](<path>) or [build/code-review/<section>.md item "<one-line>"] or <as determined for repo-root originated entries>*

**Decision:** <one sentence>

**Why:** <one paragraph including alternatives>

**Implications:** <optional>

Numbering:
- Per-feature `DECISIONS.md`: `#N` is per-feature monotonic. Read the file, take highest existing `#N`, use N+1.
- Repo-root `docs/DECISIONS.md`: independent counter, `#N` resets per file.

The inline source (Review comment or code-review item) stays in place — never deleted or rewritten. DECISIONS.md is the executive summary with a backlink; the inline doc carries the full context.
-->
