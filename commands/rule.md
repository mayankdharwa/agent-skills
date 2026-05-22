---
description: Save a coding or behavioral rule to the second brain
argument-hint: [code:|behavior:] <rule description>
allowed-tools: [Read, Write, Edit]
---

# Save Rule

Save the rule in `$ARGUMENTS` to the correct second-brain file.

## Rule to save

$ARGUMENTS

## Routing

Determine the rule type from the argument prefix:

- `code: <rule>` → save to `coding-rules.md`
- `behavior: <rule>` → save to `behavior-rules.md`
- No prefix → infer: if the rule is clearly about code style, patterns, libraries, or language conventions, treat as `code`; if it's clearly about how Claude should reason, explore, communicate, or approach tasks, treat as `behavior`. If genuinely ambiguous, ask: "Which ruleset — `code` or `behavior`?"

Strip the prefix before saving the rule text.

## coding-rules.md

Path: `/Users/mayankdharwa/Desktop/obsidian-vaults/Claude-Brain/coding-rules.md`

Template (use when creating from scratch):
```markdown
# Coding Rules

Personal rules from code reviews and experience. Claude reads these before writing code.

## General

1. <rule>
```

- Group rules by language/framework section (`## Java`, `## Python`, `## React`, etc.). Use `## General` if no specific section fits.
- Create a new section header if none exists for the language/framework.

## behavior-rules.md

Path: `/Users/mayankdharwa/Desktop/obsidian-vaults/Claude-Brain/behavior-rules.md`

Template (use when creating from scratch):
```markdown
# Behavior Rules

Personal rules for how Claude should reason, explore, and communicate.

## General

1. <rule>
```

- Group rules by topic section (`## Planning`, `## Exploration`, `## Communication`, `## Debugging`, etc.). Use `## General` if nothing fits.
- Create a new section header if none exists for the topic.

## Formatting rules (both files)

- One concise sentence per rule.
- Do not duplicate — if a similar rule exists, merge or update it.
- Preserve all existing content exactly.
- Confirm after saving: `"[code|behavior] rule saved: <one-line summary>"`
