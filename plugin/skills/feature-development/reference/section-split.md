# Section split rule

Read when a `build/testing/` or `build/code-review/` file needs structuring, or when an exploration doc gets large.

## What counts as a "section" in `build/`

A section is a cohesive unit of build work — typically a top-level service together with its private helpers and DTOs, all endpoints for one resource, or a single job. Sections are coarse: expect roughly one per top-level component in `spec/CODE-FILES.md`, not one per class. Helpers, mappers, and supporting classes belong inside the section file of the top-level component they serve.

File names match the section's primary unit, e.g., `build/testing/AssignmentService.md`, `build/code-review/AssignmentService.md`.

## Split rule

`build/testing/` and `build/code-review/` are always split per section, regardless of size. The directory of per-section files is the structure.

For other docs — exploration docs in particular — split by unit when the file crosses ~1500 lines. Check the line count at lock-time per unit; the author does not need to anticipate growth. The split creates a directory of per-unit files within the topic directory.

No `INDEX.md` files inside split directories. `PROGRESS.md` already provides cross-section status; `ls` is the structural index. Exception: `references/INDEX.md` is mandatory.
