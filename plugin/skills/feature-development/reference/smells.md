# Smells

Read when checking for state-shape problems. Surface to user; do not block. Do not silently rewrite state.

- **Two units `🚧` simultaneously** in a topic `PROGRESS.md`. Parallel work on two units is a smell — offer to defer one.
- **Deferred row that didn't resolve this pass.** At topic-lock, surface deferred `⏳` rows that never went `🚧` and ask whether they're scope change.
- **Spec distillation requiring multiple passes.** If a topic's distillation expands beyond one pass, surface as "exploration may not have actually locked."
- **One section file per class** in `build/testing/` or `build/code-review/`. Sections are coarse; helpers and mappers belong inside the top-level component's section file.
- **No `## Progress` rows in a directory where a topic/section is `🚧`.** Presence-as-signal violation.
- **`Review comment` number reuse** in an exploration doc. Within a file, numbers never reuse. On split, each callout keeps its original number — never renumber a callout. New callouts continue per-file from that file's current max.
