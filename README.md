# mayank-skills

Mayank's personal Claude Code plugin — custom skills and slash commands for day-to-day workflows.

## Structure

```
agent-skills/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest
├── skills/               # Model-invoked skills (subdirs with SKILL.md)
└── commands/             # User-invoked slash commands (.md files)
```

## Skills

| Name | Type | Description |
|------|------|-------------|
| `/side-quest <instructions>` | slash command | Delegates a task to a new agent to keep main context clean |
| `/rule <rule>` | slash command | Saves a coding rule to the second brain |
| `coding-rules` | auto-skill | Reads second-brain rules before writing any code |

---

## Adding a skill

Create a new directory under `skills/` with a `SKILL.md`:

```
skills/
└── my-skill/
    └── SKILL.md
```

`SKILL.md` frontmatter:
```yaml
---
name: my-skill
description: This skill triggers when the user asks to "..."
version: 1.0.0
---
```

## Adding a command

Create a `.md` file under `commands/`:

```yaml
---
description: Short description shown in /help
argument-hint: <arg>
allowed-tools: [Read, Bash]
---

# Command body
```

## Local registration

The plugin is registered at `~/.claude/plugins/installed_plugins.json` pointing to this directory so Claude Code picks it up on every session start.

## Testing one-off

```bash
claude --plugin-dir /Users/mayankdharwa/practo/agent-skills
```
