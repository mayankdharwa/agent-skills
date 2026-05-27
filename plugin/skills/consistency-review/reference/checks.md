# Consistency checks — issue catalogue

Read when classifying a candidate pair from `decompose.py` or a finding from
`check_links.py`. Each entry: what it is, how to spot it, how to resolve.

## Link & reference issues (from `check_links.py`)

### file-missing
A link or path mention resolves to no file (tried from the source file's dir and
the corpus root). **Resolve:** fix the path, or remove the dead reference. Check
the closest-match suggestion but confirm it's the intended target.

### anchor-missing
The file resolves but the `#anchor` matches no heading there. Usually a heading
was renamed, removed, or split out. **Resolve:** repoint to the current heading
(the suggestion is the nearest slug), or restore the heading if its removal was
the actual mistake.

### prose reference ("see file B, section E")
Not machine-checkable. Use the `--json` `heading_inventory` to find file B's real
headings. If none matches "section E", it's a stale reference — repoint or
remove. If one matches, consider converting prose into a real `path#anchor` link
so the checker can guard it next time.

### soft / bare-path findings
A bare `foo/bar.md` mention in prose that doesn't resolve. Often illustrative
(an example path, a placeholder) rather than a real link. Review, but don't
treat as a bug by default. Angle-bracket placeholders (`<path>`, `#<anchor>`)
are skipped automatically.

## Content consistency issues (from `decompose.py` edges)

### Contradiction
The two sections assert incompatible facts about the same thing — different
numbers, opposite rules, conflicting defaults (e.g. "valid 30 days" vs "valid 7
days"). **Spot:** high edge score, shared terms naming the same subject, but the
asserted values differ. **Resolve:** determine the correct value with the user,
fix the wrong one, and make one section the canonical source the other defers to.

### Leveling mismatch (the subtle one)
Same rule stated at two levels of detail: one file gives the bare rule, another
adds an exception or qualifier ("…except for service accounts"). Both are
"true," but a reader hitting only the first gets an incomplete rule. **Spot:**
high overlap, one chunk noticeably longer, contains words like *except*, *unless*,
*however*, *but*. **Resolve:** pick the canonical statement (usually the complete
one), and either have the terse one link to it or carry the same qualifier. Avoid
restating the full rule in both places — that's what desyncs.

### Terminology drift
Same concept under different names across files (e.g. "refresh token" vs "renewal
token"; "unit" vs "item"). **Spot:** edges where chunks clearly co-describe a
thing but `shared_terms` is thin because each file uses its own label; or scan
`term_index` for near-synonyms. **Resolve:** choose one term, replace the others,
re-run decompose to confirm the chunks now share the canonical term.

### Benign overlap
The sections legitimately restate shared context (a recap, a cross-reference
intro). No conflict, no hidden detail. **Resolve:** leave it. Don't manufacture
work from a high score alone — the score flags *candidates*, you make the call.

## Optional skill-format checks

Apply only when the corpus is a Claude Code skill (`SKILL.md` present):

- **Routing ↔ procedures.** Every action/procedure named in `SKILL.md`'s routing
  table should resolve to a real file (the link check covers the path; verify the
  routing description matches what the procedure actually does).
- **Template placeholders.** Template files use `<...>` placeholders; confirm
  none leaked into a rendered/instructional file as if it were real content.
- **Numbered-artifact rules.** If the skill defines ID schemes (`Q<N>`,
  `#N`, sequence numbers), they're prime contradiction sites — check the
  `term_index` for the same ID scheme described in multiple files and confirm the
  rules agree (scope, reuse, renumbering).
- **Frontmatter.** `name` matches the directory; `description` matches what the
  body actually triggers on.
