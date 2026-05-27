# Bootstrap a new feature

Create `docs/<feature>/` scaffolding for a brand-new feature. If `docs/DECISIONS.md` is missing, offer to plant it.

## Preconditions

- User intends to start a new feature.
- Feature name is known (kebab-case) or can be asked for.
- Working directory has a `docs/` (or the user agrees to create it).

## Steps

### 1. Detect missing cross-feature DECISIONS stub

Check for `docs/DECISIONS.md` (cross-feature decisions index, sparse, header only). If missing, prompt to plant a stub as part of bootstrap:

```
# Cross-feature decisions

Decisions whose scope crosses individual features.
```

If user declines, proceed.

This procedure touches only `docs/`. Anything at repo root is out of scope.

### 2. Ask for feature name

If not yet supplied. Validate: lowercase kebab-case, no spaces. Suggest the name based on what the user described.

### 3. Ask for OBJECTIVE.md content (substantive)

Walk the user through guided sections — do not write substance on their behalf:

- **What we're building** (1–3 sentences)
- **Why** (1–3 sentences — the motivation, often a constraint or stakeholder ask)
- **In scope** (bulleted list)
- **Out of scope** (bulleted list)

Capture exact phrasing. Do not rewrite.

### 4. Create the feature dir

Path: `docs/<feature>/`. Create the following silently after content is gathered:

- `OBJECTIVE.md` — from `templates/objective.md`, filled with user-provided content.
- `PROGRESS.md` — from `templates/progress-top-level.md`, with all three phase rows (`exploration`, `spec`, `build`) as `⏳`.
- `OPEN-QUESTIONS.md` — from `templates/open-questions.md`, empty index sections.
- `DECISIONS.md` — copy `templates/decisions.md` as-is. The template renders to a header + invisible HTML-comment guidance + an empty entry area; the example entry inside the template is comment-only and does not appear in the rendered file.
- `exploration/schema/` — empty dir.
- `exploration/apis/` — empty dir.
- `exploration/jobs/` — empty dir.
- `exploration/code-structure/` — empty dir.

**Do NOT create:**
- `MIGRATION-CHECKLIST.md` — created lazily on first migration item (see `procedures/migration-checklist.md`).
- `references/` and `references/INDEX.md` — created lazily on first reference (see `procedures/references.md`).
- `spec/` and its four files — created at exploration phase-lock during distillation.
- `build/` — created when build phase starts.

### 5. Summarise and propose next step

Report: feature dir created, PROGRESS state, and prompt for which exploration topic to enter first (one of: schema / apis / jobs / code-structure). Wait for the user to pick.

### 6. When user picks the first topic

Inside `exploration/<topic>/`:
- Create `<TOPIC>-EXPLORATION.md` with a one-line header (`# <Topic> exploration`).
  - `schema` → `SCHEMA-EXPLORATION.md`
  - `apis` → `API-EXPLORATION.md`
  - `jobs` → `JOBS-EXPLORATION.md`
  - `code-structure` → `STRUCTURE-EXPLORATION.md` (and later `FILE-EXPLORATION.md` if the user splits files from package layout)
- Create topic `PROGRESS.md` from `templates/progress-topic.md` with an empty `## Progress` table and a kickoff narrative in `## Current focus`. Kickoff is the highest-value moment for the narrative — a fresh session at kickoff is the most lost. The narrative carries the entry plan: which unit is up first and any context anchoring the walk (e.g., "starting with the core call-log table since downstream rows derive from it").
- Update top-level `PROGRESS.md`: flip `⏳ exploration` to `🚧 exploration`, add pointer line `- 🚧 <topic> → exploration/<topic>/PROGRESS.md`.

Prompt the user for the first unit name to add as a row.

## Errors

- Feature name already taken (dir exists): surface, ask for a different name; do not overwrite.
- `docs/` doesn't exist: create it.
- User declines the `docs/DECISIONS.md` stub: proceed; note in summary.

## Postconditions

- `docs/<feature>/OBJECTIVE.md`, `PROGRESS.md`, `OPEN-QUESTIONS.md`, `DECISIONS.md` exist.
- `docs/<feature>/PROGRESS.md` contains exactly three `⏳`/`🚧` phase rows (`exploration`, `spec`, `build`).
- `docs/<feature>/exploration/{schema,apis,jobs,code-structure}/` exist.
- If a first topic was entered: that topic's `PROGRESS.md` exists with kickoff narrative and an empty `## Progress` table; top-level `PROGRESS.md` exploration row is `🚧` with a pointer to that topic.
