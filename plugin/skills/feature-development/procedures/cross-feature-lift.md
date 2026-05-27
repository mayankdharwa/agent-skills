# Cross-feature DECISIONS lift

Promote a decision from per-feature `docs/<feature>/DECISIONS.md` to repo-root `docs/DECISIONS.md`, or originate a cross-feature decision directly at the repo level.

## When to use

- A per-feature decision has scope that crosses features (changing it would require coordinated edits in two or more feature dirs, or affects code with no feature-dir home).
- A decision is originated at repo level (no exploration backlink). Tooling adoption, repo-wide conventions, shared infrastructure choices, code-style commitments.

## Preconditions

- Repo-root `docs/DECISIONS.md` exists (planted at bootstrap if missing; otherwise create now using the same stub bootstrap uses).

## Steps

### 1. Confirm cross-feature scope (judgment)

Apply the cross-feature criteria: the standard three lift criteria (`reference/lift-criteria.md`) **PLUS** changing the decision would require coordinated edits in two or more feature dirs (or affect code with no feature-dir home).

Surface to user: the decision text, its source (per-feature DECISIONS entry, or direct origin if no exploration backlink), the one-line cross-feature reason (why a change would touch multiple feature dirs or no-feature-home code), and confirm the lift to repo-root `docs/DECISIONS.md`.

If user declines, leave the decision in per-feature scope.

### 2. Determine the next `#N` in repo-root `docs/DECISIONS.md`

Numbering is **independent** of per-feature DECISIONS files. Repo-root has its own counter. Read the file, find highest existing `## #N`, use N+1.

### 3. Determine the Source line

- **Promoted from per-feature**: `Source: [docs/<feature>/DECISIONS.md #M](docs/<feature>/DECISIONS.md)`.
- **Originated at repo level**: `Source: discussion` or `Source: <date> session notes`. The **Why** paragraph must carry the full rationale since there's no inline doc to defer to.

### 4. Write the entry

Append a new entry to `docs/DECISIONS.md` (repo root) using the canonical shape in `templates/decisions.md`. `Source:` line is per step 3 (link to the per-feature entry for promoted decisions; `discussion` or `<date> session notes` for originated-at-repo entries). For originated entries, the **Why** paragraph carries the full rationale since there is no inline doc to defer to.

### 5. Keep the per-feature entry in place (if promoted)

The per-feature `DECISIONS.md` entry stays unchanged. The cross-feature entry's `Source:` line points back to it.

### 6. Summarise

Report: the new `docs/DECISIONS.md #N`, its title, source pointer, and the state of the per-feature entry (retained, or n/a if originated at repo level).

## Sweep cadence

The repo-root file has **no scheduled sweep**. Entries land when made, or when a per-feature sweep recognises cross-feature scope. The repo-root file stays sparse by design — entries should be rare.

## Errors

- Repo-root `docs/DECISIONS.md` doesn't exist: create it as a stub (same as bootstrap would), then proceed.
- Source per-feature entry doesn't exist (user pointed at a non-existent `#M`): surface; ask whether to originate the entry or fix the pointer.
- The decision is clearly per-feature (only one feature dir affected): surface; recommend keeping it per-feature.

## Postconditions

- `docs/DECISIONS.md` (repo root) contains a new `## #N` entry with `<N>` one greater than any pre-existing entry in THAT file (counter independent of per-feature `DECISIONS.md`).
- The new entry's `Source:` line points at the per-feature entry (if promoted) or carries `Source: discussion` / dated session notes (if originated).
- If promoted: the per-feature entry is unchanged at its original location.
