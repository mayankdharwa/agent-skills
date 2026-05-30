# Custom topic shape

Read when working with `exploration/custom/`. Establishes file-level structure, lock granularity, and distillation fold rules. Lifecycle steps live in `procedures/custom.md`.

## When custom belongs (and when it doesn't)

`custom/` is the escape hatch for design work that doesn't fit `schema`, `apis`, `jobs`, or `code-structure` — and isn't reference material about an existing external system. Single test: **Does this sub-exploration design new artifacts the feature is introducing that don't fit one of the standard four topics?** If yes, `custom/` is the right home. If it's reference material about an existing external system, route to `references/` instead.

Typical fits: vendor integration shapes (e.g., new Exotel applet designs, new webhook contracts a vendor will ingest), new external file/template designs, new event taxonomies, vendor-side configuration that the feature owns the design of.

Typical misfits: internal API design (→ `apis/`); legacy code mapping (→ `references/`); a single one-off decision that fits in an existing topic's callout.

## File-level structure

```
exploration/custom/
  INDEX.md                          stable nav, no status
  PROGRESS.md                       standard topic progress; units = sub-explorations
  _archive/
    PROGRESS_<YYYY-MM-DD>_<seq>.md  archived at topic-lock
  <sub-exploration>/                flexible internal shape; drafted via authoring workflow
    ...                             filenames not prescribed
  <sub-exploration>/
    ...
```

### `INDEX.md`

Stable navigation. One line per sub-exploration. No status emoji. Updated only when a sub-exploration is added (or when a sub-exploration is dropped via scope change). Survives topic-lock — does not archive.

```markdown
# Custom explorations

One line per sub-exploration: short hook describing what it covers and when to read it. Stable nav — no status here; status lives in PROGRESS.md.

- [exotel-applets/](exotel-applets/) — Shape of new Exotel applets for Vox→customer call flows
- [prescription-templates/](prescription-templates/) — Layouts for new prescription PDFs
```

The hook is what a future CLAUDE.md reader scans to decide whether any of this design work applies to their current task. Make it specific.

### `PROGRESS.md`

Standard topic progress per `templates/progress-topic.md`. Units are sub-exploration names. Lock granularity is the sub-exploration. Archives at topic-lock per the normal flow.

### Sub-exploration folder

Internal structure is flexible — the skill does not prescribe filenames. Common shapes:

- A single `<NAME>-EXPLORATION.md` (mirrors standard-topic shape).
- A primary doc plus auxiliary files (`flow-diagrams.md`, `applet-1.md`, `applet-2.md`).
- A nested `PROGRESS.md` of the sub-exploration's own units, if the sub-exploration is large enough to warrant finer-grained tracking. Optional — the parent `custom/PROGRESS.md` row is the lock that matters.

## Authoring workflow inside a sub-exploration

The agent drafts content collaboratively with the user — it does not leave the folder empty for the user to populate alone. The loop:

1. **Agree on structure.** Ask the user what shape the sub-exploration takes (single doc vs primary + auxiliary vs nested-PROGRESS) and what sections the primary doc needs. Write the outline file(s) — headings only, plus a one-line hook under each describing what the section will cover.

2. **Estimate size and pick a cadence.** Anticipate how large the document will get and confirm the cadence with the user before drafting. Two options:
   - **Whole-doc, then item-by-item review.** Draft every section in one pass, then walk the user through the inline questions one at a time.
   - **Section-by-section.** Draft one section, user reviews and answers its questions, draft the next. Use this when the doc is large or when later sections depend on decisions made in earlier ones.

3. **Fill sections the agent understands.** Where the meaning of a section is clear from the outline and from material in `references/`, draft it using the agent's understanding of the domain. Pull from `references/<file>.md` where applicable.

4. **Mark unknowns inline.** Anywhere the agent is guessing, missing context, or sees a branch the user needs to decide, drop a blockquote callout in place:
   ```markdown
   > **Question:** <one specific question>

   > **Note for user:** <observation or assumption the user should confirm>
   ```
   If you find yourself about to draft a passage in a spot you don't actually understand, stop and add the callout instead. If a section can't be drafted without an answer, write the callout and leave the section stubbed.

   These callouts are **scaffolding**, not the decision record. Unlike `Review comment #N` callouts (which persist as the durable decision record at sub-exploration lock) and `OPEN-QUESTIONS.md` entries (which persist across phases), `Question:` / `Note for user:` callouts are removed once the answer is incorporated in step 5. None should remain in the doc at lock time.

5. **Surface questions one at a time.** After drafting (whole-doc cadence) or after each section (section-by-section cadence), walk the user through the inline callouts one by one. Incorporate each answer into the prose and remove the callout. If a question can't be answered now, route to `OPEN-QUESTIONS.md` per `procedures/defer.md` and remove the inline callout (it now lives as a deferred question, not scaffolding). Durable decisions worth preserving are *not* minted as `Review comment #N` during the authoring loop — they are formalised at sub-exploration lock via `procedures/custom.md`, which routes through `procedures/unit-lock.md` and carries the lock ritual (user confirmation, monotonic numbering, decision/why content).

6. **Lock the sub-exploration** once every section is filled and every inline callout is resolved — sub-exploration lock per `procedures/custom.md`.

The user remains the authority: every draft is a proposal, and the user can rewrite, restructure, or scrap it. The agent's job is to do the legwork — propose structure, fill what it can, surface what it can't — not to gatekeep the shape.

## Lock granularity

Three lock layers when `custom/` is active:

| Scope | Action | Where status lives |
|---|---|---|
| Sub-exploration | `procedures/custom.md` sub-exploration lock (mirrors `procedures/unit-lock.md`) | Row in `custom/PROGRESS.md` |
| Custom topic | `procedures/topic-lock.md` with `custom` as the topic | `custom/PROGRESS.md` archives; pointer removed from top-level |
| Exploration phase | `procedures/distill.md` (after all live topics — standard four + custom if it exists — are locked) | Top-level `exploration` → `✅` |

Internal sub-exploration files (if the user maintains a nested PROGRESS.md inside a sub-exploration folder) are user-tracked — the skill does not gate sub-exploration lock on internal sub-rows. The user declares the sub-exploration ready; the skill performs the row flip.

## Review comment callouts inside custom

The DECISIONS-sweep at custom-topic-lock walks all `.md` files inside `custom/` (excluding `INDEX.md`, `PROGRESS.md`, anything under `_archive/`) and finds every `Review comment #N` callout. Same sweep logic, same lift criteria as standard topics.

Callout numbering: per-file monotonic (`reference/sequence-rules.md`). Each internal file in each sub-exploration has its own `#N` counter. On file split inside a sub-exploration, the per-file rule applies as in standard topics.

If a user has not used Review comment callouts inside a sub-exploration (because they tracked decisions in some other way), surface at sub-exploration lock: "no callouts found in this sub-exploration — do decisions need to be added before lock, or is this intentional?"

## Distillation fold rules

At exploration phase-lock, `procedures/distill.md` walks all live topics. For each sub-exploration in `custom/`, the user names one or more fold targets:

- One of the four standard spec files (`SCHEMA.md`, `APIS.md`, `JOBS.md`, `CODE-FILES.md`).
- A new spec file (e.g., `spec/INTEGRATIONS.md` for vendor-side artifacts) — created during distillation if named.

Multiple fold targets are valid: e.g., `exotel-applets` may fold into both `APIS.md` (the webhook endpoints Vox exposes) and a new `spec/INTEGRATIONS.md` (the vendor-side applet shape itself).

The user names the fold target(s) at distillation time, not earlier — the choice is a function of what crystallised during exploration, not a pre-commitment.

## Top-level PROGRESS.md interaction

While `custom/` is live and exploration is active, the pointer line appears:

```
- 🚧 exploration
  - 🚧 apis → exploration/apis/PROGRESS.md
  - 🚧 custom → exploration/custom/PROGRESS.md
```

Pointer lifecycle is symmetric with standard topics: **added when the topic activates** (lazy-create of `custom/` for the custom topic; first unit/sub-exploration entered for a standard topic), **removed at topic-lock**. Exploration phase-lock requires every live topic pointer to have been removed — the standard four plus `custom` if it was ever created.

If `custom/` is never created, the exploration phase-lock gate is unchanged — only the standard four need to lock.

## Smells specific to custom

- **An empty sub-exploration folder at sub-exploration-lock time.** Either it should be dropped via scope change, or the user hasn't actually done the work — surface.
- **A sub-exploration that fits a standard topic.** If the user names a sub-exploration like `user-endpoints`, surface: this looks like `apis/` work. Confirm intent before creating the folder.
- **INDEX.md row count differs from `custom/` subfolder count.** Drift — surface and ask whether to reconstruct.
- **A sub-exploration with no `Review comment` callouts at lock time.** Surface: confirm decisions live elsewhere or add them before lock.
- **User declares sub-exploration ready while their nested `PROGRESS.md` (if any) still shows `🚧` rows.** The skill doesn't gate on internal sub-rows (see "Lock granularity" above), so this state is invisible to the lock action — surface as a smell so the user can decide whether they're locking prematurely.
