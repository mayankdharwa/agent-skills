# Project-done check

Verify all three gates for project-done and produce a status report.

## Preconditions

- Feature dir is active.

## The three gates

The three gates:

1. Top-level `PROGRESS.md` is all-`✅`.
2. `OPEN-QUESTIONS.md` `## Index (active)` is empty.
3. Every `Mandatory` item in `MIGRATION-CHECKLIST.md` is closed.

Note: `Independent and Important` and `Optional` migration items do NOT gate project-done. They may remain open indefinitely.

## Steps

### 1. Check Gate 1 — top-level PROGRESS

Read `docs/<feature>/PROGRESS.md`. Confirm every phase row is `✅`. The three rows are:
- exploration
- spec
- build

`references/` is a sidecar — no phase row. Absence of an active `references/PROGRESS.md` is sufficient; references are supporting material, not gating deliverables.

If any row is not `✅`, list which.

### 2. Check Gate 2 — OPEN-QUESTIONS active index

Read `docs/<feature>/OPEN-QUESTIONS.md`. Count entries under `## Index (active)`.

If non-zero, list them.

### 3. Check Gate 3 — Mandatory MIGRATION-CHECKLIST items

If `docs/<feature>/MIGRATION-CHECKLIST.md` exists:
- Parse `###` items grouped under `##` team headings.
- Filter to those carrying the `[Mandatory]` tag.
- For each, check the `Status:` line. Closed items show `[x] Done — YYYY-MM-DD`.
- List any pending Mandatory items.

If `MIGRATION-CHECKLIST.md` doesn't exist, the gate passes by vacuity.

### 4. Report

Produce a tabular status report:

```
Project-done check for <feature>:

Gate 1 (top-level PROGRESS all-✅):       [PASS | FAIL]
  <if FAIL, list non-✅ rows>

Gate 2 (OPEN-QUESTIONS active empty):     [PASS | FAIL]
  <if FAIL, list active Q-numbers>

Gate 3 (Mandatory migration closed):      [PASS | FAIL | N/A>
  <if FAIL, list pending Mandatory items by ID>

Overall: [PROJECT DONE | NOT DONE — see failures]
```

### 5. Heads-up: open `TD<N>` items

If `docs/<feature>/TECH-DEBT.md` exists, count entries whose `Status:` is `[ ] Pending`. If the count `K > 0`, append a non-blocking line to the report:

```
Heads-up (non-blocking): <K> open TD item(s) in TECH-DEBT.md.
```

If `K == 0` (or the file does not exist), emit nothing. Heads-up only; not a gate — see `reference/tech-debt-shape.md` "Project-done gate".

### 6. If all gates pass

Report: all three gates pass; the project is done. Mention what stays in place (top-level `PROGRESS.md` at all-`✅` never archives; the feature dir is historical documentation, do not delete unless docs drift from code), what's archived (all non-top-level `PROGRESS.md` files, already moved during normal phase termination), the list of any open `Independent and Important` migration items (these may remain open indefinitely), the count of any open `TD<N>` items (non-blocking; may remain open indefinitely), and prompt the user to consider whether to announce or change project status (e.g., release note).

### 7. If gates fail

Surface the report as-is. Do NOT auto-resolve any of the failures. The user must:
- Close out remaining `🚧` phase work (route to relevant procedure).
- Resolve remaining active OPEN-QUESTIONS entries (`procedures/open-questions.md` resolve mode).
- Close remaining Mandatory migration items (`procedures/migration-checklist.md` close mode).

## Errors

- Required file missing (e.g., `OPEN-QUESTIONS.md` doesn't exist): drift — surface; treat as fail for that gate.
- Parser unable to determine status (malformed PROGRESS.md or MIGRATION-CHECKLIST.md): surface; refuse to declare PASS/FAIL.

## Postconditions

- A report exists (in the user-facing summary) listing each gate's PASS/FAIL with specifics.
- No files in the feature dir are mutated by this procedure — it is read-only.
