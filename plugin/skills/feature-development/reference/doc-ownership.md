# Doc ownership

Read before editing any tracked file. Edits land per the role and the path.

- `exploration/<topic>/*-EXPLORATION.md`, topic `PROGRESS.md` — edit freely.
- `build/testing/<section>.md`, `build/PROGRESS.md` — edit freely.
- `build/code-review/<section>.md` — Review Agent + Coding Agent both write here. Review Agent appends findings; Coding Agent tags them (`fixed` / `wont-fix:` / `decision:` / `spec-changed:`). Pure mechanical fixes made by the Coding Agent during its own work need no entry.
- `OPEN-QUESTIONS.md` — add entries freely. Resolving requires user confirmation.
- `spec/*`, `OBJECTIVE.md`, `DECISIONS.md`, `MIGRATION-CHECKLIST.md`, `references/*` — confirm with user before any edit.
- `_archive/*` — never edit. Only move files in.
