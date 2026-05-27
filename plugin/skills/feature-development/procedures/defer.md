# Defer a unit

Skip a unit in the current pass and come back later. Deferral is temporary; the row stays `⏳` and carries an inline `— deferred: <pointer>` marker.

## Preconditions

- A topic is active.
- The unit being deferred exists as a `🚧` or `⏳` row in the topic's `PROGRESS.md`.

## Steps

### 1. Ask the two-path question (substantive)

Surface the framing verbatim — leading with the user's own state, not procedural labels:

> Do you know what to do? *(You'll find out offline; I add an open question and we come back at end of walk.)*
> OR
> Should I create a reference document? *(You list the questions; I research; the unit waits on the reference.)*

Wait for the user to pick the offline-resolves path or the research path.

### 2a. If path 1 (offline-resolves)

Ask the user for the question text (1–3 sentences). Then route to `procedures/open-questions.md` (add) to create a new `OPEN-QUESTIONS.md` entry with:
- Next monotonic Q-number.
- A `blocks: <unit>` line.

Capture the Q-number returned.

Update the deferred row to:
```
- ⏳ <unit> → <doc> §N — deferred: BLOCKED by Q<N>
```

### 2b. If path 2 (research path)

Ask the user for the list of questions the reference should answer.

Check whether `references/PROGRESS.md` exists:
- If yes: add a row for the new reference job.
- If no: create `references/` directory; create `references/PROGRESS.md` from `templates/progress-topic.md` and add the row.

Decide on a reference filename based on what's being researched (kebab-case, descriptive). Surface to user for confirmation.

Update the deferred row to:
```
- ⏳ <unit> → <doc> §N — deferred: awaiting references/<file>.md
```

Note: the actual reference document creation is a separate step — see `procedures/references.md`. Bootstrap of references/PROGRESS row is enough here.

### 3. Update narrative

The `## Current focus` paragraph names the next non-deferred `⏳` unit. The `Next up:` line continues to the next non-deferred unit. Append a "Deferred so far:" line if multiple have been deferred.

Example after deferring `vn_destinations`:
```
Next up: vn_assignment (SCHEMA-EXPLORATION.md §7). Deferred so far: vn_destinations (Q12).
```

### 4. Summarise

Report: which unit was deferred, which path was taken, the deferral pointer (Q-number or reference filename), and the next unit.

## Loop-back at end of walk

After the last non-deferred unit in the topic finishes, `procedures/topic-lock.md` handles loop-back to deferred rows. This procedure does NOT preempt loop-back.

## Errors

- User refuses both paths: surface that deferral requires a target; ask if they meant to lock the unit instead.
- The user's question or research list is empty: prompt for content; don't write a placeholder.

## Postconditions

- The unit's row in topic `PROGRESS.md` is `⏳` and carries an inline `— deferred: <pointer>` marker (either `BLOCKED by Q<N>` or `awaiting references/<file>.md`).
- The deferral pointer is real: `OPEN-QUESTIONS.md` contains `Q<N>` with a `blocks:` line, OR `references/PROGRESS.md` contains a row for the awaited reference filename.
