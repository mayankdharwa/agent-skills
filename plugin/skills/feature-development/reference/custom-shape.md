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
  <sub-exploration>/                user-defined internal structure
    ...                             user names files; skill does not prescribe
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

User-defined internal structure. The skill never prescribes filenames inside. Examples of shapes users might choose:

- A single `APPLETS-EXPLORATION.md` (mirrors standard-topic shape).
- A primary doc plus auxiliary files (`flow-diagrams.md`, `applet-1.md`, `applet-2.md`).
- A nested `PROGRESS.md` of the sub-exploration's own units, if the sub-exploration is large enough to warrant finer-grained tracking. Optional — the parent `custom/PROGRESS.md` row is the lock that matters.

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
