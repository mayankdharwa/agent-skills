---
name: polish-language
description: Polish a single markdown/text file to strip residual "we used to do X, now Y" framing left by iterative edits — prose that encodes revision history instead of stating current truth. Requires an explicit file path; do not auto-trigger. One file per invocation.
version: 1.0.0
allowed-tools: [Read, Edit]
---

# polish-language

After a few rounds of edits, documents accumulate scar tissue: phrasings that carry the editing history instead of the current meaning. This skill rewrites those passages as if the doc were being written from scratch today.

User-invoked only. Always takes an explicit path to a single file:

```
Skill(skill="polish-language", args="<path-to-file>")
```

If invoked without a path, stop and ask for one. Do not guess from conversation context. If the user wants to polish several files, they'll invoke the skill once per file (or ask the agent to loop over a list they provide) — this skill itself only handles one file per run.

## Examples of the pattern

| Carries history | Reads as current truth |
|---|---|
| "Durable conventions that apply when writing code, not just reviewing" | "Durable conventions that apply while writing and reviewing code" |
| "We previously allowed greenfield at `docs/` but now require `docs/<feature>/`" | "Every feature roots at `docs/<feature>/`" |
| "Sections used to live under `exploration/` only; now `build/` also has sections" | "Sections live under `exploration/` and `build/`" |
| "We no longer use Redis; everything goes through Postgres" | "All state lives in Postgres" |
| "This is the Review Agent now (was Code Review Agent earlier)" | "This is the Review Agent" |

> **Note on the first row — "not just X":** This phrasing is the closest call in the tells list. It's *history-residue* when the surrounding doc already integrates X as a peer of the original scope (the "not just" is redundant). It's *load-bearing* when X is the reader's default assumption and the contrast actively redirects them. When unsure, treat as **ask**.

## Tells

These phrasings often indicate residual history. See "When to keep" for the exceptions.

- "not just X" / "no longer X" / "rather than X" — when X is the doc's previous wording
- "previously" / "we used to" / "in the past" / "earlier"
- "instead of X, we do Y"
- "X, not Y" — when both are mentioned only to contrast the change (history-residue if Y is the doc's previous wording; load-bearing if X and Y are both current options a reader might confuse — treat as **ask** when unsure)
- A scope/qualifier appended to a sentence that contradicts the sentence's start
- A first clause stating an old state, followed by "but" / "however" / "now"
- Parentheticals like "(was X)" / "(formerly X)" / "(previously called X)"

## When to keep historical framing

The contrast IS the meaning — leave the phrasing alone — when:

- The doc is a CHANGELOG, migration note, ADR, or release note. History is its purpose.
- A reader is likely to arrive expecting the old behavior and needs redirecting (deprecation pointers to paths or names still in circulation).
- The contrast is between two genuinely current options a reader might confuse — e.g., "Auth tokens are HS256, not RS256" where both are plausible defaults — not between current and past behavior. (Distinguish from the Tells-table row "We no longer use Redis; everything goes through Postgres", which IS history because Redis was previously in use here.)
- Removing the contrast loses a non-obvious constraint a reader would re-derive incorrectly.

When in doubt, ask the user before stripping.

## Procedure

1. **Resolve the target.** Confirm the path resolves to a single file. If it's a directory or glob, stop and ask the user to pick one file. If the filename matches `CHANGELOG*`, `ADR-*`, sits under an `adr/` or `adrs/` dir, contains `migration`, or is a release note, surface that — those docs keep history by design — and ask whether to proceed anyway.
2. **Scan for the tells above.** Read the file top to bottom; collect candidate passages with `line` references. Quote the original line verbatim. Skip text inside YAML frontmatter, fenced code blocks, indented code blocks, blockquotes, and tables — these are usually deliberate examples, quotations, data, or metadata, not the doc's own voice. If a tell appears in one of those regions and looks like it might actually be the doc's voice (e.g., a blockquote used as a callout), flag it as **ask**, never auto-rewrite. If the scan finds no candidates, say so and stop.
3. **Classify each candidate.**
   - **Rewrite** — the "before" half is dead weight; the sentence becomes a clean present-tense statement.
   - **Keep** — the contrast is load-bearing (see "When to keep").
   - **Ask** — unclear without user context.
4. **Propose rewrites in batch.** Present candidates using this shape, with "rewrite" and "ask" groups separated. Do not apply yet. If candidates exceed ~20, batch by section and get approval iteratively rather than dumping everything at once.

   ```
   Rewrites (apply all on OK):
   - L42: "<original>" → "<proposed>" — <one-line why>

   Asks (confirm each):
   - L88: "<original>" — <what's ambiguous, what context would resolve it>
   ```
5. **Apply on approval.** Rewrite items: apply the whole batch on a single user OK (don't ask per item). Ask items: confirm each individually before applying or dropping. Use `Edit` for each accepted item.
6. **Re-scan after edits.** A rewrite occasionally surfaces another stale contrast in adjacent prose (e.g., a paragraph that explains the "before" the rewritten line no longer references). Walk the file once more. Stop when a full pass finds no new candidates, or after two re-scans — whichever comes first.

## Notes

### Rewrite rules

- The fix is almost always shorter than the original. If your rewrite is longer, you probably reintroduced the history — default to the shorter version.
- Preserve voice and register. The polished sentence should sound like the rest of the doc, not like a different author wrote it.

### When to stop and ask

- Don't invent facts to fill the rewrite. If the current truth isn't deducible from the doc, ask the user — do not infer from filenames, git log, or memory.
- If a rewrite would erase information the project might want preserved (a deprecation, a renamed concept still in circulation externally, a non-obvious "why we moved off X"), flag it and ask whether to move that content into a CHANGELOG, ADR, or migration note rather than deleting it outright.
- This skill changes wording, not structure. If a section's purpose has shifted, that's an editing task, not a polish — surface it and stop.
