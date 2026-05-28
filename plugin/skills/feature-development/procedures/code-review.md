# Code review (build phase — Review Agent entry)

The entry point when the skill is invoked in the **Review Agent** role (the invocation
declares it, e.g. "You are the Code Review Agent"; see SKILL.md "Role declaration on
invocation"). The skill defaults to the Coding Agent — this procedure runs only under
an explicit Review Agent declaration.

Governs the *ceremony* of reviewing: where to look, where findings land, the finding and
resolution shapes, and the verify-then-tag loop. The *substance* of the review — what to
flag — is the agent's judgement. The checklist in step 3 is a prompt, not a gate.

## Preconditions

- Build phase is active: `build/` exists and `build/PROGRESS.md` has at least one section row.
- At least one section has code to review — a row with `code: 🚧` (code in progress) or
  `tests: ✅ · code: 🚧`. A section with `code: ⏳` and no code yet has nothing to review.

If build phase is not active, surface and stop — there is no code-review work outside build.
If invoked in the Review Agent role but no section has code, say so and stop.

Roles, ownership, and the tag set: `reference/doc-ownership.md`. Lock/archive flow:
`reference/lock-semantics.md`, `procedures/section-archive.md`.

## Steps

### 1. Detect the section under review

Standard state detection has already run (SKILL.md). From `build/PROGRESS.md`:

- One section with reviewable code → that section.
- Several → list them with their `tests:`/`code:` status and ask which to review. Remember
  the choice in conversation context.

Read the section's `build/testing/<section>.md` (what the tests assert, what they don't)
and `build/code-review/<section>.md` if it already exists (prior findings, which carry
Coding Agent responses awaiting verification — step 4).

### 2. Read the code under review

Identify the code for this section from the testing doc and `build/PROGRESS.md` pointers.
Read it. This is a fresh, independent read — do not assume the Coding Agent's framing.

### 3. Conduct the review

What to flag is your judgement. The following dimensions are a non-binding prompt — skip
any that don't apply, add any the code warrants:

- **Correctness** — does it do what the testing doc and spec say? Edge cases, off-by-one,
  null/empty, concurrency.
- **Error handling** — structured errors with error codes; failures surfaced, not swallowed
  (Practo convention).
- **Logging / observability** — structured JSON logging, correlation IDs on the request path.
- **Practo conventions** — feature-based organisation, naming, the patterns in any
  `.claude/memory/patterns-learned.md`.
- **Test coverage** — do the tests in `testing/<section>.md` actually cover the code's
  branches? Gaps are findings too.
- **Security** — input validation, authz checks, no secrets in code/logs, injection surfaces.
- **Clarity / maintainability** — naming, dead code, duplication, comment density matching
  the surrounding file.

Pure-mechanical nits the Coding Agent would obviously fix need not become findings unless
they recur or matter; prefer signal over volume.

### 4. Append findings and run the verify-then-tag loop

The Review Agent owns `build/code-review/<section>.md`. If it doesn't exist, create it
(`# Code review — <section>` heading, then findings). Append each finding using
`templates/code-review-finding.md`. Number per-file monotonic (`Finding #N`) —
`reference/sequence-rules.md`.

For each finding, the cycle is:

1. **You append the finding.** Stop there for new findings — the Coding Agent responds next.
2. **Coding Agent appends a response block** under the item — `> **Coding Agent response**`,
   shape in `reference/doc-ownership.md`. You do not write that block.
3. **You independently verify against the code** — re-read the changed code; do not trust the
   response's claim. Then append the `> **Resolution:**` tag line (shape in
   `templates/code-review-finding.md`) as the item's final line:
   - `fixed` — verified the change resolves it.
   - `wont-fix: <reason>` — agreed it should not change.
   - `decision: <text>` — resolved by a recorded user/judgement call (record the call).
   - `spec-changed: <link>` — needs a locked-spec change; link the surgical-reopen/OPEN-QUESTIONS entry.
4. **Agree-but-out-of-section-scope.** When the Coding Agent's response is "valid
   observation, out of section scope," do not auto-tag. Surface to the user — they decide
   whether to log it as a TD entry (`procedures/tech-debt.md` Add mode → then tag the
   finding `wont-fix: see TD<N>`) or close without one (`wont-fix: <reason>`). The user's
   call, not the Review Agent's. The Review Agent never invokes `procedures/tech-debt.md`
   itself.
5. **Disagree with a refusal?** Leave the item **untagged** and append a follow-up finding
   under it. An untagged item blocks `section-archive` (`procedures/section-archive.md`),
   which forces another response cycle or a user tie-break. Do not tag to unblock.

Never edit the Coding Agent's response lines. Never write a `> **Coding Agent response**` block.

### 5. Route issues that aren't plain code findings

If something you find isn't a straightforward code fix — needs user input, needs a locked
spec changed, or belongs elsewhere — route via `reference/issue-routing.md` instead of (or
in addition to) a finding. One issue lands in exactly one place.

### 6. Hand back

Once you've posted findings (or verified responses and tagged), summarise per SKILL.md:
what you reviewed, how many findings at each severity, how many tagged vs awaiting Coding
Agent response, and whether the section is now fully tagged (ready for `section-archive`).

Do not archive from this procedure unless explicitly asked — archive is a separate lifecycle
action (`procedures/section-archive.md`) and the Coding Agent or user typically triggers it.

## Errors

- Build phase not active → surface, stop.
- No section has reviewable code → surface, stop.
- Section name doesn't match any `build/PROGRESS.md` row → drift; surface and ask.
- `code-review/<section>.md` exists but for a section not in `build/PROGRESS.md` → drift; surface and ask.

## Postconditions

- `build/code-review/<section>.md` exists with each new finding appended in the canonical shape, numbered per-file.
- For every finding that had a Coding Agent response, you have either appended a verified Resolution tag or left it untagged with a follow-up finding.
- No Coding Agent response lines or tags were written by anyone but their owner.
- `build/PROGRESS.md` and `build/testing/<section>.md` are untouched by this procedure (status flips happen at section-archive; testing-doc edits are the Coding Agent's).
