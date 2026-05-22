---
description: Delegate a task to a new agent to conserve main context
argument-hint: <task instructions>
allowed-tools: [Agent]
---

# Side Quest

Delegate the task to a new agent. **Never attempt the work yourself** — always use the Agent tool. This command exists specifically to keep the main conversation context clean.

## Task

$ARGUMENTS

## How to delegate

1. Identify context the agent needs to succeed without any prior conversation history:
   - Current working directory
   - Tech stack / language / framework
   - Relevant background from this conversation (bugs found, decisions made, constraints)
   - Whether the agent should only research or also make changes

2. Write a self-contained agent prompt that briefs the agent like a smart colleague who just walked into the room. Include everything they need; omit anything that isn't load-bearing.

3. Call Agent with a concise description (3–5 words) and the self-contained prompt.

4. Present the agent's result to the user. Summarize only if the raw result is very long — otherwise return it as-is. Do not re-investigate or redo any of the agent's work.
