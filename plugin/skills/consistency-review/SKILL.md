---
name: consistency-review
description: Use when reviewing a set of markdown files (a skill, a docs/ tree, a spec — usually 5+ files) for INTERNAL consistency. Catches cross-file contradictions / duplicated rules at differing levels of detail, and broken cross-file links and heading anchors. Runs two deterministic scripts first, then narrows the agent's reading to only the suspicious spots.
version: 1.0.0
---

# consistency-review

Review a set of markdown files for **internal consistency** — not grammar,
not structure (leave those to your own judgment), but two specific defects that
get worse as the file count grows:

1. **Contradiction / duplication.** One file says "the rule is X"; another says
   "the rule is X but with exception Y". The rule is now defined in two places,
   at two levels of detail. Fixing one silently desyncs the other.
2. **Broken cross-references.** A file points at `other.md#section-e` (or just
   says "see other file, section E") but that heading no longer exists.

Reading every file and eyeballing it is expensive and non-repeatable. This skill
front-loads **two deterministic scripts** that narrow your attention to the few
places that actually need human judgment.

This is general-purpose: it works on any folder of markdown. Skill-format
knowledge (frontmatter, action-routing tables) is layered as optional checks in
`reference/checks.md`, not assumed.

## Tools

Both are pure-stdlib Python (`python3`, no install). Paths are relative to this
skill directory.

- `scripts/check_links.py <dir>` — verifies links and `#anchor`s deterministically.
- `scripts/decompose.py <dir>` — builds a cross-file similarity graph.

`<dir>` is the corpus root (the folder whose files you're reviewing) — **any**
folder of markdown, not just a skill.

## General documents

The tools are domain-agnostic; point them at any markdown corpus and the same
5-step procedure applies. For example, reviewing a product spec split across
several files:

```
python3 scripts/check_links.py ~/work/payments-spec
python3 scripts/decompose.py  ~/work/payments-spec
```

Then prompt: *"review these docs for internal consistency."* Skip the
skill-format checks in `reference/checks.md` — they only apply when the corpus
is a Claude Code skill (`SKILL.md` present). Everything else (contradiction,
leveling mismatch, terminology drift, broken links) is general.

**Tuning for non-skill corpora.** Defaults (`--threshold 0.25`, `--min-tokens
10`) were calibrated on a code-like skill. For prose-heavy docs with long
sections, raise `--threshold` to cut benign overlap; for terse reference docs,
lower it to catch thinner matches. It's deterministic, so iterate freely.

## Procedure

### 1. Link check (deterministic — fully solves problem 2)

```
python3 scripts/check_links.py <dir>
```

- Stderr prints a human summary; stdout prints the JSON findings.
- Exit code is non-zero when any **hard** finding exists (file-missing or
  anchor-missing). **Soft** findings (bare `.md` path mentions in prose) don't
  fail — review them but don't assume they're bugs.
- Each finding carries a closest-match suggestion. Use it, but confirm against
  the target before rewriting — the nearest slug isn't always the intended one.
- For natural-language references the script can't resolve ("see the section on
  X"), pull the **heading inventory**: `python3 scripts/check_links.py <dir> --json`
  emits `heading_inventory` (every file's real headings + slugs). Map the prose
  reference onto a real heading; if none fits, that's a finding.

Fix or report each hard finding. Do not auto-rewrite prose references without
confirming intent.

### 2. Decompose into a similarity graph (narrows problem 1)

```
python3 scripts/decompose.py <dir>
```

- Stderr prints the **top candidate pairs** — sections across different files
  that likely describe the same thing. Stdout prints the full JSON graph
  (`nodes`, `edges`, `clusters`, `term_index`).
- An edge means "these two sections probably talk about the same rule." A high
  score (cosine + shared rare terms) means strong overlap. `shared_terms` tells
  you *why* they were paired — often the rule name itself.
- `term_index` lists defined terms that appear across 2+ files — a direct
  duplicate-definition radar.

### 3. Pointed review (this is where your judgment goes)

Open **only** the chunks named in the top edges and term-index entries — not the
whole corpus. For each candidate pair, read both sections and classify against
`reference/checks.md`:

- **Contradiction** — the two state incompatible facts (30 days vs 7 days). Fix.
- **Leveling mismatch** — same rule, but one adds an exception/qualifier the
  other omits. Decide the canonical statement; make the other defer to it or
  carry the same qualifier.
- **Benign overlap** — they legitimately restate shared context. Leave it.
- **Terminology drift** — same concept, different names across files. Unify.

Walk edges top-down; stop when scores fall to clearly-unrelated pairs.

### 4. Report and fix

Produce a findings list (source locations + classification + proposed change).
Apply fixes the user approves. Prefer making one section the canonical
definition and having others reference it, over restating the rule in full
twice — that's what created the drift.

### 5. Re-run both scripts (closes the "fix-one-break-another" loop)

After edits:

```
python3 scripts/check_links.py <dir>     # a rename may have broken an anchor
python3 scripts/decompose.py <dir>       # a reword may have created a NEW near-duplicate
```

This is the step that makes consistency work convergent instead of
whack-a-mole. Repeat 3–5 until link check is clean and no new high-score edge
appeared that you haven't judged.

## Notes

- The engine is lexical and deterministic by design: same input → same graph,
  no API, repeatable in CI. Its blind spot is a contradiction with **zero**
  shared vocabulary (pure synonyms). In practice contradictions share terms (the
  rule name, the IDs, the units), so this is rare — but if you suspect a
  synonym-only conflict, the `term_index` and your own reading are the backstop.
- Tunables: `decompose.py --threshold` (edge cutoff, default 0.25),
  `--min-tokens` (filters content-thin heading-only chunks, default 10),
  `--top` (summary length). `check_links.py --soft-hard` fails on bare-path
  findings too.
- See `reference/checks.md` for the full catalogue of issue types and how to
  judge each, including the optional skill-format checks.
