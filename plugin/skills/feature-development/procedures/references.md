# References lifecycle

Add a reference document. References cache knowledge from outside the codebase being built — legacy code maps, library docs, prior art. Created lazily; per-reference lock.

## Preconditions

- Feature dir is active.
- User has identified knowledge worth caching (e.g., from a research session, a legacy code dive, or a deferred unit's research path).

## Steps

### 1. Confirm the reference is worth writing

Apply the trigger: would re-creating this from scratch later be painful? If the user just wants quick notes that won't be re-read, suggest they skip references and inline the knowledge wherever it lands. References are for cached knowledge with re-derivation cost.

### 2. Lazy-create `references/` if missing

If `docs/<feature>/references/` doesn't exist:
- Create the directory.
- Create `references/INDEX.md` with header only:
  ```markdown
  # References

  One line per reference file: short hook describing what it covers and when to read it.
  ```

### 3. Lazy-create `references/PROGRESS.md` if reference work is active

Create `references/PROGRESS.md` when either condition holds:
- User is creating multiple references as a batch (e.g., "mapping the legacy Fabric codebase" — multi-session work).
- A unit is deferred via the research path (`procedures/defer.md`) and is awaiting this reference. Presence of `references/PROGRESS.md` signals "research is in flight" for the loop-back at topic-lock.

In both cases:
- If `references/PROGRESS.md` doesn't exist, create it from `templates/progress-topic.md` with kickoff narrative and the new references as `🚧` rows.
- If it exists, add the new reference as a `🚧` row.

If this is a single one-off reference not triggered by a defer and not part of a batch, no `references/PROGRESS.md` needed.

### 4. Get reference filename and content from user

Ask the user:
- Filename (kebab-case, descriptive of content).
- Content (substantive — user writes the reference; skill does not synthesize).

If the reference is the result of a research path from `procedures/defer.md`, the user already listed the questions; the reference should answer them.

### 5. Write the reference file

Path: `docs/<feature>/references/<filename>.md`.

The file is locked when written — references are write-once cached knowledge, not iterative docs.

### 6. Update `INDEX.md` (mandatory in same change)

Append a one-line entry:
```
- [<filename>.md](<filename>.md) — <short hook describing what it covers and when to read it>
```

The hook is what `CLAUDE.md` readers scan to decide if any cached research applies to their current task. Make it specific.

### 7. Update `references/PROGRESS.md` if applicable

Flip the row for this reference from `🚧` to `✅`. If this was the last row in the batch, archive `references/PROGRESS.md`:
- Path: `references/_archive/PROGRESS_<YYYY-MM-DD>_<seq>.md`
- Sequence: per-directory monotonic.

### 8. Resolve any deferred unit waiting on this reference

If a `⏳ ... — deferred: awaiting references/<this-file>.md` row exists in any topic `PROGRESS.md`, surface: which unit, which topic, that the reference is now available, and ask whether to lock the unit. If user says yes, route to `procedures/unit-lock.md` for that unit.

### 9. Summarise

Report: which reference file was written, INDEX.md updated, and whether any deferred unit is now ready to lock.

## Staleness

If a reference document goes stale, **archive it under `references/_archive/`** and write a new one. Do NOT mutate in place. To handle:
- Ask user to confirm stale.
- Archive path: `references/_archive/<file>_<YYYY-MM-DD>_<seq>.md`. `<seq>` per `reference/sequence-rules.md` (per-reference-file monotonic across time).
- Move existing file: `git mv references/<file>.md references/_archive/<file>_<YYYY-MM-DD>_<seq>.md`.
- Remove its line from `INDEX.md`.
- Route to "add new reference" (Steps 4–6 above) for the replacement.

## Errors

- Filename collision: surface; suggest a more specific name.
- `INDEX.md` is missing when references already exist: drift — surface and offer to reconstruct from `ls references/`.
- User wants the skill to write substance: refuse; references are user-written cached knowledge.

## Postconditions

- `docs/<feature>/references/<filename>.md` exists.
- `docs/<feature>/references/INDEX.md` contains a one-line entry for `<filename>.md`.
- If a batch is active: the reference's row in `references/PROGRESS.md` is `✅`. If batch is complete, `references/PROGRESS.md` is in `_archive/` with proper per-directory sequence.
