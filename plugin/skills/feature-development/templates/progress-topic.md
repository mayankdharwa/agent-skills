<!-- Replace placeholders in <angle-brackets> when filling this in. -->

## Current focus

**<unit-name>** — <short qualifier>

<2–3 line state summary: what's been locked, what's blocking, what was last touched. Points at exploration / code-review / OPEN-QUESTIONS docs; does not restate substance.>

Next up: <next concrete step — next unit / next section>.

## Progress

- ⏳ <unit-name> → <doc-pointer>
- ⏳ <unit-name> → <doc-pointer>

<!--
Row discipline: rows carry status icon + pointer + optional inline `— BLOCKED by Q<N>` / `— deferred: <pointer>` markers only. No rationale, no findings, no "noticed that X" notes. Substantive discussion lives in the exploration callouts / OPEN-QUESTIONS / code-review / DECISIONS.

Narrative edge states for `## Current focus`:

Kickoff (nothing started yet — highest-value moment for the narrative; a fresh session at kickoff is the most lost):

> **vn_call_log** — entry point for the schema walk
>
> Starting with vn_call_log since downstream rows (vendor_callbacks, vn_assignment)
> all carry foreign keys back to it. No locks yet; no open questions.
>
> Next up: vn_call_log (SCHEMA-EXPLORATION.md §3).

All-✅, pre-archive (collapses to one line):

> Topic locked. All units ✅ — running DECISIONS.md sweep, then archive.

Surgical reopen (header reads `## Current focus — surgical reopen`):

> **vn_call_log** — adding `cid` column
>
> Triggered by code-review/AssignmentService.md item "missing correlation ID on
> outbound webhook payload". Single-unit reopen.
>
> Next up: (none — single-unit reopen).
-->
