# Sequence numbering rules

Read when generating or validating a sequence number for an archive filename or a numbered artifact (`#N`, `Q<N>`, `Review comment #N`, migration item ID).

## Archive sequences

- **`build/code-review/<section>_<YYYY-MM-DD>_<seq>.md`** — per-section monotonic across time. Each section has its own counter that increments across archives. Counter does **not** reset per day. Two archives of the same section on different days continue the same sequence.
- **`PROGRESS_<YYYY-MM-DD>_<seq>.md` in any `_archive/`** — per-directory monotonic across time. Each directory has its own counter. Does **not** reset per day.
- **`references/_archive/<file>_<YYYY-MM-DD>_<seq>.md`** — per-reference-file monotonic across time. Each archived reference filename has its own counter.

## Numbered artifacts

- **`Q<N>` in `OPEN-QUESTIONS.md`** — per-feature monotonic. Numbers never reuse, even when resolved.
- **`Review comment #N`** — per-file monotonic. On file split, each callout keeps its original number — never renumber. Backlinks resolve via `<file-path>:#<N>`; after a split, only the file-path portion of the backlink updates, the number stays. New callouts in either split child continue per-file from that file's current max.
- **Migration item IDs (`V1`, `V2`, `F1`, ...)** — per-team monotonic. Prefix is the first letters of the owning team's `##` heading.
- **`DECISIONS.md #N`** — per-feature monotonic. Repo-root `docs/DECISIONS.md` has its own independent counter.

## How to determine the next sequence

Read the existing files / entries in the relevant scope. Find the highest existing number. Use that + 1. If nothing exists, start at 1.

Never reuse numbers, even after deletions or scope changes.
