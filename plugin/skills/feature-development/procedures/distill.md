# Spec distillation

One-pass distillation across all four spec files at exploration phase-lock. Triggered when all four topics are locked. Writes locked, clean reference material — no review comments, no open questions, no alternatives.

## Preconditions

- All four exploration topics are locked (`exploration/<topic>/PROGRESS.md` exists in none of them — only in `_archive/`).

## Steps

### 1. Create `spec/` directory

`mkdir docs/<feature>/spec/`.

### 2. Walk the four spec files

The four files are written together in one pass — do not lock one before starting the next. Cross-topic discoveries during distillation may require all four to be revised. **If distillation requires a second pass on the same file, that's a smell — surface to user that exploration may not have actually locked.**

For each file:

#### `spec/SCHEMA.md` — locked DDL

From `exploration/schema/SCHEMA-EXPLORATION.md` (plus any split files):
- Extract every `✅` unit (each table/column/index/FK).
- Write the DDL representation. No callouts, no alternatives.
- Group logically (tables together, indexes/FKs after).
- Each unit's locked decisions become facts of the DDL — they're already the decision.

#### `spec/APIS.md` — locked HTTP surface

From `exploration/apis/API-EXPLORATION.md`:
- Extract every locked endpoint.
- Format: path, method, request/response shape, auth, error codes.
- Group by resource.

#### `spec/JOBS.md` — locked background work

From `exploration/jobs/JOBS-EXPLORATION.md`:
- Extract every locked worker, cron, queue topology.
- Format: name, trigger (cron expr / queue), inputs, outputs, idempotency notes, schedule.

#### `spec/CODE-FILES.md` — locked file/class plan

From `exploration/code-structure/STRUCTURE-EXPLORATION.md` (and `FILE-EXPLORATION.md` if it exists):
- New files: path + one-line purpose.
- Modifications to existing files: path + what changes.
- Top-level services, controllers, jobs, DTOs.

### 3. Draft all four files together, then write

Draft `spec/SCHEMA.md`, `spec/APIS.md`, `spec/JOBS.md`, `spec/CODE-FILES.md` in parallel based on locked exploration. **Surface all four drafts together** before writing any to disk — a cross-topic discovery in one draft may force revision in another, and locking one file first would force a second pass on the others.

Each draft includes a one-line summary of contents (e.g., table count, endpoint count). User reviews all four; confirms or asks for revisions. Apply revisions. Write all four to disk in one step.

Lean on mechanical organisation (grouping, extracting from callouts), not judgment — locked decisions ARE the spec.

**Voice rule for spec files:** no review comments, no open questions, no alternatives. Spec files read in present tense as if the final choice was always the choice. Alternatives and history belong in exploration callouts and `DECISIONS.md`.

### 4. Update top-level `PROGRESS.md`

- Flip `🚧 exploration → ✅`.
- `⏳ spec` does NOT get its own `🚧` phase — distillation is the spec phase. Flip directly: `⏳ spec → ✅`.
- The `⏳ build` row stays `⏳` until the user is ready to start build.

The `spec` phase has no `PROGRESS.md` of its own (no `spec/PROGRESS.md`). Distillation is single-pass; absence of progress tracking is intentional.

### 5. Confirm spec phase

Report distillation complete, exploration and spec rows now `✅`, and prompt the user for the first build section to enter (typically a top-level service from `CODE-FILES.md`). Build start is gated on the user's readiness, not the skill's.

## Errors

- Distillation requires a second pass on the same file: surface as smell — "exploration may not have actually locked; reopen the relevant topic instead?"
- A spec file would be empty (no locked content for that aspect): surface to user — is this expected (e.g., no APIs in this feature)? If yes, write the file with a one-line `No <X> changes for this feature.` placeholder. If no, distillation is premature.
- Cross-topic discovery during distillation: stop, surface, ask whether to surgical-reopen the relevant topic before continuing.

## Postconditions

- `docs/<feature>/spec/SCHEMA.md`, `APIS.md`, `JOBS.md`, `CODE-FILES.md` all exist.
- No `docs/<feature>/spec/PROGRESS.md` exists (spec has no progress tracker by design).
- Top-level `PROGRESS.md` shows `exploration ✅` and `spec ✅` — the `spec` row goes straight from `⏳` to `✅`, never `🚧`.
