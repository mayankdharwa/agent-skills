---
name: feature-development
description: Use when bootstrapping a new feature under `docs/<feature>/`, locking units, deferring questions, distilling spec, archiving build sections, surgically reopening locked phases, or checking project-done. Operates a three-phase exploration → spec → build process for medium-to-large backend features.
---

# feature-development

Drive the multi-phase development of a feature. The user contributes substance; the skill handles ceremony — dirs, files, callout formats, archives, sequence numbers, lifecycle transitions.

This skill is suggest-only. Wait for explicit invocation; the agent may recommend it when the conversation enters lifecycle territory.

Do not engage for bugfixes, small refactors, single-file edits, or tasks expected to wrap in under a few hours.

## Roles

- **Coding Agent** — drives work across phases. The skill, when invoked, acts as the Coding Agent **by default**. In code-review, appends a `> Coding Agent response:` block under each item (action taken or refusal reason). Does not write tag lines.
- **Review Agent** — owns `build/code-review/<section>.md`. Appends findings, and after the Coding Agent posts a response, independently verifies against the code and writes the resolution tag (`fixed` / `wont-fix:` / `decision:` / `spec-changed:`). Entered by an explicit role declaration at invocation (see below); its build-phase entry and loop are `procedures/code-review.md`.
- **User** — locks decisions, confirms protected-doc edits, answers open questions, breaks ties when Review Agent and Coding Agent disagree.

### Role declaration on invocation

The skill operates as **one** role per session. Default is the Coding Agent. To run as the Review Agent instead, the invocation declares it — e.g. starting a fresh session and invoking the skill with a prompt like "You are the Code Review Agent" (or "Review Agent"). Treat any such role-naming declaration as selecting that role for the whole session.

Run state detection either way (below). Then route by role: a Review Agent declaration with build phase active → `procedures/code-review.md`. No declaration → Coding Agent; route by the action as usual. The two roles never edit each other's lines in `build/code-review/<section>.md` (see `reference/doc-ownership.md`).

In the build phase, the cycle is TDD: write tests → write code → review → respond → independently verify and tag → repeat. Each section in `build/` carries dual test+code status (see `templates/progress-build.md`).

## Operating posture

1. **Tiered autonomy.** Execute pure mechanics silently after the higher-level action is approved. Checkpoint once at phase/scope transitions (sweep, archive, distillation, surgical reopen entry). Prompt the user for substantive content (Review comment text, OBJECTIVE body, OPEN-QUESTIONS phrasing, cleanup-vs-meaning judgment).
2. **Read all state on every invocation.** Run `ls docs/`. Read the active feature's top-level `PROGRESS.md`, any active topic `PROGRESS.md`, `OPEN-QUESTIONS.md` index. State files are the cursor; never maintain a sidecar.
3. **Surface smells; do not block.** See `reference/smells.md`.
4. **Surface inconsistencies; never auto-sync.** When a state file drifts from reality, ask the user what to do.
5. **Bootstrap missing cross-feature scaffolding.** If `docs/DECISIONS.md` is missing when the user starts work, offer to plant a stub before creating the feature dir. Bootstrap touches only `docs/`; anything at repo root is out of scope.
6. **Enumerate multi-question turns.** When surfacing three or more decisions in a single turn, number them so the user can answer by index.
7. **Confirm before moving to the next step.** Once all open items in a phase or section resolve, confirm before proceeding.
8. **End with a tight summary.** Three to six lines: what changed, the next concrete step, any smells or deferred items.

## State detection on invocation

1. `ls docs/` — locate feature dirs (dirs containing `OBJECTIVE.md`). 0 → bootstrap mode. 1 → auto-pick. 2+ → ask which one; remember in conversation context.
2. Read `docs/<feature>/PROGRESS.md`. Identify which of the three phase rows (`exploration`, `spec`, `build`) is `🚧`. `references/` is a sidecar — no phase row.
3. If a phase row is `🚧`, read the pointer it carries (e.g., `→ exploration/schema/PROGRESS.md`) for the active topic / section.
4. Read `OPEN-QUESTIONS.md` index to know what's blocked.
5. Route by role and action (see below). Under a Review Agent declaration with build phase active, route to `procedures/code-review.md`.

If `PROGRESS.md` is malformed or unreadable, surface and ask. Do not guess.

## Action routing

- Start a new feature / no feature dir exists → `procedures/bootstrap.md`
- Lock a unit / approve a unit → `procedures/unit-lock.md`
- Defer a unit / can't lock yet → `procedures/defer.md`
- Topic done / all rows `✅` in topic → `procedures/topic-lock.md`
- All exploration topics locked / ready to distill spec → `procedures/distill.md`
- Invoked as Review Agent / review the active build section → `procedures/code-review.md`
- Section done / all `code-review/<section>.md` items tagged → `procedures/section-archive.md`
- Surgically reopen / proposed edit to `spec/*` → `procedures/surgical-reopen.md`
- Add open question / resolve `Q<N>` → `procedures/open-questions.md`
- Add a reference / new doc in `references/` → `procedures/references.md`
- Add migration item / close `<id>` → `procedures/migration-checklist.md`
- Decision affects multiple features → `procedures/cross-feature-lift.md`
- Is the project done / final gate check → `procedures/project-done-check.md`
- An issue surfaced mid-work / unclear where to log it → `reference/issue-routing.md`

Each procedure file is self-contained: preconditions, steps, errors, postconditions. Read the procedure when routing to it.

## Reference files

Read on-demand when the topic comes up:

- `reference/sequence-rules.md` — archive sequences (`<seq>` resolution), numbered artifacts (`#N`, `Q<N>`, `Review comment #N`, `Finding #N`, migration IDs).
- `reference/smells.md` — state-shape problems to surface.
- `reference/section-split.md` — when a `build/` or exploration file needs splitting; also the positive definition of a section.
- `reference/doc-ownership.md` — edit rules per path.
- `reference/lift-criteria.md` — the three lift criteria, sweep cadences, immediate-lift mechanics.
- `reference/issue-routing.md` — the "Where does this go?" decision rule for mid-work issues.
- `reference/lock-semantics.md` — the three lock scopes (unit / topic / phase) and the phase-termination gates.
- `reference/migration-checklist-shape.md` — file-level structure, item ID, tags, and item shape for `MIGRATION-CHECKLIST.md`.

## File templates

Read the template before writing a new artifact:

- `templates/objective.md` — feature `OBJECTIVE.md`.
- `templates/progress-top-level.md` — feature top-level `PROGRESS.md`.
- `templates/progress-topic.md` — exploration topic `PROGRESS.md` and `references/PROGRESS.md` (with `## Current focus`).
- `templates/progress-build.md` — `build/PROGRESS.md`. Section rows carry dual test+code status (e.g., `· tests: ⏳ · code: ⏳`).
- `templates/open-questions.md` — feature `OPEN-QUESTIONS.md`.
- `templates/decisions.md` — feature `DECISIONS.md`.
- `templates/review-comment.md` — inline `Review comment` callout.
- `templates/code-review-finding.md` — `build/code-review/<section>.md` finding item (Review Agent), with the response-block and resolution-tag shapes.
