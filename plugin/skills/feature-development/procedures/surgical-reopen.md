# Surgical reopen

When work in a later phase reveals a gap in an earlier locked phase. The response depends on whether the spec edit changes the *meaning* of the locked spec.

## Preconditions

- User has identified a gap or proposed an edit to a `spec/*` file (or `OBJECTIVE.md`, or other locked content).
- The relevant phase is already locked (otherwise this is normal in-phase work).

## Step 1: Cleanup vs. meaning-change judgment (pre-judge, confirm with user)

Apply the boundary test:

**Meaning change** if the edit:
- Adds, removes, or renames a table, column, endpoint, field, job, class.
- Changes a type or contract.
- Reorders invariants.
- Anything where a future Coding Agent reading only the spec doc (no git history) would derive a different design from before and after the edit.

**Cleanup edit** if the edit is:
- Typo.
- Formatting.
- Broken internal link.
- Clarifying prose with no semantic change.

Surface your judgment to the user:

> Proposed edit to `<file>`:
> ```
> <diff>
> ```
> Judgment: **<meaning change | cleanup edit>**.
> Reason: <one-line rationale based on the rule>.
> Confirm / flip?

**When ambiguous, default to meaning change.** Surgical reopen is recoverable ceremony; silent meaning-change-as-cleanup corrupts the spec lineage.

## Step 2a: If CLEANUP — confirm-and-edit

1. Apply the edit in place.
2. No `Review comment` callout.
3. No `PROGRESS.md` resurrection.
4. No `DECISIONS.md` consideration.
5. Git commit (when the user commits) is the record.

Report: cleanup edit applied to which file; no process artifacts created.

## Step 2b: If MEANING CHANGE — full surgical reopen

Six steps in order:

### Step 2b.1: Create a new `PROGRESS.md`

Determine which topic the edit belongs to:
- `spec/SCHEMA.md` → `exploration/schema/`
- `spec/APIS.md` → `exploration/apis/`
- `spec/JOBS.md` → `exploration/jobs/`
- `spec/CODE-FILES.md` → `exploration/code-structure/`

Create new `exploration/<topic>/PROGRESS.md` (NOT edit an archive). Use `templates/progress-topic.md` with `## Current focus — surgical reopen` header and a narrative naming the unit being reopened and the trigger. Initial row: one `🚧` row for the unit being reopened. Presence of this file signals the phase is reopened.

### Step 2b.2: Add a new `Review comment` callout

Ask the user for the substantive content (why the reopen is needed, alternatives considered, trade-off). Append a `Review comment #N` callout in the topic's `*-EXPLORATION.md` (next monotonic number per `reference/sequence-rules.md`; never reuse, even across split files). Use `templates/review-comment.md`.

If the trigger came from a `build/code-review/<section>.md` item, include a `Triggered by:` line linking to it.

### Step 2b.3: Edit the spec doc in place

Apply the user-proposed edit to the spec file. **No changelog in the doc. No version markers. The doc reads as if it were always this way.**

Confirm with user before writing — the spec is confirm-before-edit per `reference/doc-ownership.md`.

### Step 2b.4: Lift to `DECISIONS.md` if course-altering

Apply the three lift criteria from `reference/lift-criteria.md`. If the decision qualifies, append to `DECISIONS.md` with backlink to the new Review comment. Cross-feature check: if the decision affects code outside this feature, also route to `procedures/cross-feature-lift.md`.

### Step 2b.5: Backlink from the trigger

If the surgical reopen was triggered by a `build/code-review/<section>.md` item, edit that item to add the tag:

```
spec-changed: see exploration/<topic>/<TOPIC>-EXPLORATION.md §N (Review comment #M)
```

### Step 2b.6: Archive the new `PROGRESS.md`

Flip the `🚧` row to `✅`, then archive:

- Path: `exploration/<topic>/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md`
- `<seq>` per `reference/sequence-rules.md` (per-directory monotonic across time — resumes from prior archives).

End-of-procedure summary: surgical reopen complete for `<topic>/<unit>`; the new Review comment number and location; the spec file edited; whether a DECISIONS entry was lifted; whether a code-review item was tagged `spec-changed`; the archive path of the resurrected `PROGRESS.md`.

## Errors

- User explicitly disagrees with the judgment (says cleanup when skill said meaning change): respect user's call but surface the risk one more time. If user insists, treat as cleanup but DO NOT apply silently — confirm again.
- Spec file has been hand-edited outside this skill since last lock: surface as drift.
- The trigger is a `build/code-review/<section>.md` item that doesn't exist or is already archived: surface and ask user to clarify which item is being addressed.

## Postconditions

**Cleanup edit:**
- Spec file is edited at the expected location. No new artifacts.

**Meaning change:**
- A new `Review comment #N` exists in the topic's exploration doc with a monotonic number greater than any pre-existing callout.
- The spec file is edited in place (no version markers, no changelog inside the doc).
- If lifted: `DECISIONS.md` has a new entry with `Source:` backlinking to the new Review comment.
- If trigger was a code-review item: that item carries a `spec-changed:` tag pointing at the new Review comment.
- A resurrected `exploration/<topic>/PROGRESS.md` does NOT exist at the live path; an archive `_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md` exists with the next monotonic `<seq>` for that directory.

## Breaking-change exception

If the change breaks a previously shipped contract (deployed v1 API changing), surface that this is a breaking change to a shipped contract. Suggest the options: in-place edit, version the spec (e.g., `spec/APIS.md` → `spec/APIS-v2.md`), or write a migration note. Wait for the user to choose. Do not version automatically — versioning has cascading implications the user must own.
