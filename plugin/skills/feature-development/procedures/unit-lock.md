# Unit-lock

Lock one unit in an exploration topic. A unit is a table, endpoint, job, or class — anything that gets one row in a topic `PROGRESS.md`.

## Preconditions

- A feature dir is active.
- A topic is active (top-level `PROGRESS.md` shows `🚧 <topic> → exploration/<topic>/PROGRESS.md`).
- The unit being locked exists as a `🚧` row in that topic's `PROGRESS.md`.
- The user has provided substantive content for the Review comment callout (decision + why, alternatives considered).

If the unit row is `⏳` (not yet started), promote it to `🚧` silently as part of this action.

If the unit doesn't exist as a row yet, that's a drift case — surface and ask whether to add the row first or whether the user named the wrong unit.

## Steps

### 1. Confirm the lock with the user

Confirm before mutating. Communicate: which unit, which file the callout will land in, the next Review comment number, and that the row will flip to `✅`. Wait for explicit confirmation.

Determine `#N`: read the exploration file, find the highest existing `Review comment #M`, use M+1. Never reuse numbers (see `reference/sequence-rules.md`).

Determine `§X`: the section in the exploration doc where the unit is defined.

### 2. Append the Review comment callout

Format: `templates/review-comment.md`.

Date is today (use `date +%Y-%m-%d`). Decision and Why come from the user. Triggered-by is optional; include only if the lock was triggered by an existing code-review item or `OPEN-QUESTIONS.md` entry.

### 3. Update topic `PROGRESS.md`

In the `## Progress` table, flip the row icon from `🚧` to `✅`. Row format stays unchanged otherwise:

```
- ✅ <unit> → <TOPIC>-EXPLORATION.md §X
```

Update the `## Current focus` narrative:
- If there's a next non-deferred `⏳` unit: name it as the new focus. Update the narrative to reference what was just locked.
- If no non-deferred `⏳` rows remain (everything else is `✅` or `⏳ ... — deferred:`): set narrative to:
  > All non-deferred units ✅. Routing to topic-lock.

  Then route to `procedures/topic-lock.md`. Topic-lock handles the case-split: if deferred rows exist, it runs loop-back; if not, it proceeds to the sweep + archive. Unit-lock does not prejudge which path.
- The `Next up:` line names the next non-deferred `⏳` unit, or `(none — routing to topic-lock)` if none remain.

### 4. Check for smells

After the row flip, scan for smells (see `reference/smells.md`):
- Two `🚧` rows simultaneously → surface to user.
- Newly-introduced `Review comment #N` number that collides with existing — should never happen if step 1 was followed correctly.

### 5. Summarise

Report: which unit locked, which Review comment number landed where, topic progress count (N of M units `✅`), and what's next (next unit, or that topic-lock is triggered).

## Errors

- Unit name doesn't match any row: drift — surface, ask whether to add row.
- `<TOPIC>-EXPLORATION.md` doesn't have a §X for this unit: drift — surface, ask whether to add the section.
- Two `🚧` rows after the lock attempt resolved: this means the user has split focus; surface as smell.

## Postconditions

- A new `Review comment #N` callout exists in the topic's `*-EXPLORATION.md` with a monotonic number greater than any pre-existing callout.
- The unit's row in topic `PROGRESS.md` shows `✅`.
- The `## Current focus` narrative names a different unit (or the topic-lock pre-archive line).
