# Doc ownership

Read before editing any tracked file. Edits land per the role and the path.

**Ownership applies to content edits, not lifecycle moves.** Archive moves (`git mv <file> _archive/...`), file splits, and renames are lifecycle transitions executed by whichever procedure owns the transition. They do not require the file-owner role to perform them. The relevant procedure gates the move with its own preconditions (e.g., section-archive requires every item Review-Agent-tagged before moving `code-review/<section>.md`).

- `exploration/<topic>/*-EXPLORATION.md`, topic `PROGRESS.md` — edit freely.
- `exploration/custom/INDEX.md`, `exploration/custom/PROGRESS.md`, `exploration/custom/<sub-exploration>/*.md` — edit freely (same posture as standard exploration topics). The skill handles bookkeeping: directory creation, appending INDEX.md hook lines, adding/flipping PROGRESS.md rows. The authoring loop inside a sub-exploration folder is described in `reference/custom-shape.md`; lifecycle in `procedures/custom.md`.
- `build/testing/<section>.md`, `build/PROGRESS.md` — edit freely.
- `build/code-review/<section>.md` — Review Agent owns the file. Review Agent appends findings (shape in `templates/code-review-finding.md`; entry + loop in `procedures/code-review.md`) and, after independently verifying the Coding Agent's work, writes the resolution tag (`fixed` / `wont-fix: <reason>` / `decision: <text>` / `spec-changed: <link>`). Coding Agent appends a `> **Coding Agent response**` block (shape below) under each item — one line describing the action taken or, for a refusal, the reason — but does not write tag lines. Neither role edits the other's lines. Pure mechanical fixes made by the Coding Agent during its own work (not surfaced by a Review Agent) need no entry.

  Response block shape:
  > **Coding Agent response** *(YYYY-MM-DD)*
  >
  > **Action:** fixed | refused | deferred | spec-change-needed
  > **Detail:** <one line — what was changed, or why refused, or pointer to OPEN-QUESTIONS / surgical-reopen>

  Review Agent reads the response, verifies against the code, and writes the tag. If the Review Agent disagrees with a refusal, it leaves the item untagged and appends a follow-up finding — the section cannot archive until every item carries a tag, which forces resolution.
- `OPEN-QUESTIONS.md` — add entries freely. Resolving requires user confirmation.
- `spec/*`, `OBJECTIVE.md`, `DECISIONS.md`, `MIGRATION-CHECKLIST.md`, `TECH-DEBT.md`, `references/*` — confirm with user before any edit.
- `_archive/*` — never edit. Only move files in.
