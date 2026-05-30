# Custom topic lifecycle

The `exploration/custom/` topic is an optional 5th exploration step for sub-explorations that don't fit the standard four (`schema`, `apis`, `jobs`, `code-structure`). Typical fit: vendor integration artifacts that the feature *designs* but that live outside the codebase (e.g., new Exotel applet shapes, new external webhook contracts, new email template designs). Reference material *about* the existing external system belongs in `references/`; design of the *new* artifacts belongs here.

Lazy-created on first sub-exploration. Each sub-exploration is the unit of lock. Internal structure inside a sub-exploration folder is user-defined — the skill enforces only the topic-level shape (INDEX.md, PROGRESS.md, archive layout). See `reference/custom-shape.md`.

## Preconditions

- Feature dir is active.
- User has identified a body of design work that doesn't fit the standard four topics. If it fits one of the four, route there instead — `custom/` is the escape hatch, not the default.
- For a new sub-exploration entry: a kebab-case sub-exploration name and a one-line hook for INDEX.md.

## Add a sub-exploration

### 1. Confirm the sub-exploration is worth a folder

Apply the gate: does this body of work warrant a folder of its own? If it's a single decision or a single document, it likely belongs inline in an existing topic or as a single `references/` file. Custom sub-explorations are multi-file, multi-decision bodies of work.

### 2. Get sub-exploration name and hook from user

Ask:
- **Folder name** — kebab-case, descriptive (e.g., `exotel-applets`, `prescription-templates`).
- **INDEX.md hook** — one line: what this sub-exploration covers, when a future reader should open the folder.

Validate the folder name doesn't already exist under `custom/`.

### 3. Lazy-create `custom/` if missing

If `docs/<feature>/exploration/custom/` doesn't exist:

1. Create the directory `exploration/custom/`.
2. Create `exploration/custom/INDEX.md` with header only:
   ```markdown
   # Custom explorations

   One line per sub-exploration: short hook describing what it covers and when to read it. Stable nav — no status here; status lives in PROGRESS.md.
   ```
3. Create `exploration/custom/PROGRESS.md` from `templates/progress-topic.md` with an empty `## Progress` table and a kickoff narrative in `## Current focus` naming the sub-exploration from step 2 as the first focus. Mirrors `procedures/bootstrap.md` step 6 for standard topics — table starts empty; the row is added in step 6 below.
4. Update top-level `PROGRESS.md`: if `🚧 exploration` is already active, add pointer line `- 🚧 custom → exploration/custom/PROGRESS.md` under it. If exploration was `⏳`, flip to `🚧` and add the pointer.

If `custom/` already exists, skip to step 4.

### 4. Create the sub-exploration folder

Create `exploration/custom/<sub-exploration>/`. Leave it empty. The user populates internal structure as they explore — the skill does not prescribe filenames inside.

### 5. Update INDEX.md

Append one line:
```
- [<sub-exploration>/](<sub-exploration>/) — <hook>
```

INDEX.md is stable navigation; no status emoji here. Status lives in `custom/PROGRESS.md`.

### 6. Update `custom/PROGRESS.md`

Add a row to `## Progress` as `⏳` (consistent with how new units are added to standard topics — promotion to `🚧` happens when the user starts work):
```
- ⏳ <sub-exploration> → exploration/custom/<sub-exploration>/
```

One `🚧` at a time per `reference/smells.md` — when the user starts work on this sub-exploration, promote silently to `🚧`.

### 7. Summarise and propose next step

Three to six lines per `SKILL.md` Operating posture rule 8. Cover: sub-exploration folder created, INDEX.md hook added, PROGRESS.md row state, and an explicit Next up — ask the user what they want to draft first inside the sub-exploration folder (the first internal file, an outline, a flow diagram, etc.). The skill does not author the content; the prompt anchors the user's next action.

## Sub-exploration lock

The unit-of-lock in `custom/` is the sub-exploration (one PROGRESS.md row per sub-exploration). Lock semantics mirror `procedures/unit-lock.md` with these differences:

- The Review comment callout lands in whichever internal file inside the sub-exploration the user designates. The skill does not prescribe a filename — at first lock, ask the user which file in `custom/<sub-exploration>/` holds the decisions; on subsequent locks within the same sub-exploration, re-read the folder to find existing `Review comment` callouts and continue per-file numbering.
- If the user maintains decisions across multiple internal files, each file carries its own `Review comment #N` counter (per-file monotonic, per `reference/sequence-rules.md`). The sweep at custom-topic-lock walks all `.md` files in `custom/<sub-exploration>/` to find callouts.
- Row format on flip: `- ✅ <sub-exploration> → exploration/custom/<sub-exploration>/<decisions-file>` — the pointer names the file the user designated for decisions. If decisions live in multiple files, the pointer names the folder (`exploration/custom/<sub-exploration>/`).

Otherwise — confirmation, sequence-number determination, `## Current focus` update, smell checks — proceed as in `procedures/unit-lock.md`.

If no non-deferred `⏳` rows remain after the lock, route to `procedures/topic-lock.md` with `custom` as the topic. Topic-lock works unchanged: it walks the topic's `.md` files for `Review comment` callouts (in `custom/`, this means walking all sub-exploration folders) and runs the DECISIONS sweep.

## Deferral

A sub-exploration can be deferred like any unit. Route to `procedures/defer.md`. The row becomes:
```
- ⏳ <sub-exploration> — deferred: <pointer to OPEN-QUESTIONS Q<N> or references/<file>.md>
```

Deferred sub-exploration rows participate in the loop-back at custom-topic-lock the same way deferred unit rows participate in standard-topic-lock — see `procedures/topic-lock.md` step 1.

## Errors

- Sub-exploration folder name collision: surface; ask for a more specific name.
- INDEX.md missing when sub-exploration folders already exist: drift — surface and offer to reconstruct from `ls custom/`.
- User wants the skill to author internal sub-exploration content: refuse; custom is user-driven by design.
- User tries to add a sub-exploration that clearly fits an existing topic (e.g., a new internal API): surface and suggest routing to the appropriate topic instead.

## Postconditions

- `exploration/custom/INDEX.md` contains one line per sub-exploration.
- `exploration/custom/PROGRESS.md` has one row per sub-exploration with its current status icon — `⏳` until work starts, `🚧` while in flight, `✅` once locked.
- Each sub-exploration has its own folder under `custom/`; internal structure is user-defined.
- Top-level `PROGRESS.md` has `- 🚧 custom → exploration/custom/PROGRESS.md` under `🚧 exploration` while the topic is active.
