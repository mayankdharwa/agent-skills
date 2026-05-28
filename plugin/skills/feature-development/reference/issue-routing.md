# Where does this go?

Read when an issue surfaces mid-work — a question, a finding, a concern, or a fix — and it is unclear where to log it. This rule picks *which* artifact to touch; the action-routing table in `SKILL.md` then picks the procedure that touches it.

Apply in order:

1. **Answerable or applicable now without user input?**
   - Exploration: no — exploration decisions need user lock. Skip to step 2.
   - Build, mechanical fix by the Coding Agent: apply. *Only if a Review Agent surfaced it*, append a `> **Coding Agent response**` block under the item describing the action; the Review Agent verifies and writes the `fixed` tag. Otherwise no entry.

2. **Needs user input now and user is available?** Discuss → lock as a `Review comment` callout (exploration; route to `procedures/unit-lock.md`) or, for a build code-review item, the Coding Agent records the user's call in its response block and applies the change; the Review Agent verifies and writes the `decision: <text>` tag.

3. **Needs user input later?** Route to `procedures/defer.md`. The two-path question creates an `OPEN-QUESTIONS.md` entry with `blocks:` or a reference-creation job under `references/`. The current row gets a `— deferred: <pointer>` marker.

4. **Resolution requires modifying a locked spec?** Route to `procedures/surgical-reopen.md`. Trigger is recorded wherever the issue surfaced.

**One-shot rule:** every issue lands in exactly one place. If it changes form (e.g., an open question becomes a decision), update the original entry to point to the new home — do not duplicate.

## Out-of-tree procedures

Two procedures are user-invoked and intentionally not enumerated above. The decision tree does not route to them; the user invokes them directly when the observation fits.

- `procedures/migration-checklist.md` — work owned by another team or in another codebase. Use when the issue isn't fixable inside this feature's tree at all.
- `procedures/tech-debt.md` — own-codebase, non-blocking code-quality follow-up (refactor, naming, util extraction, "do it this way not that way"). Use when the code works but warrants a later cleanup pass. Not a resolution path for Review Agent findings.

If an observation matches one of these, do not force it through the four-step tree — invoke the procedure directly.
