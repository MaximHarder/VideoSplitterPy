# Skill routing by phase

Read a skill immediately before its operation, not all skills before the first
question. Discover paths through [Cursor runtime](cursor-runtime.md).
Announce switches as "Using [skill] to [purpose]". The phase order in `SKILL.md`
and the overrides below take precedence over supporting skills.

| Phase | Required skills and overrides |
| --- | --- |
| Enter planning | `using-superpowers` first. Override its brainstorm-before-Plan-mode step: enter Plan mode before exploration or other skills. |
| Evidence/delegation | `create-subagent` for briefing shape, not permanent agent installation. Context skills only when used, per [delegation](context-management.md). |
| Interview | `brainstorming`, `grill-with-docs`, then its required `grilling` and `domain-modeling`. Design, glossary, and decisions live in `plan.md`; no spec commit, repo-root `CONTEXT.md`, or separate ADR. |
| OKR | `okr-strategist` when the approach and Language are settled. Use its drafting phases, quality checklist, and output format inside the existing OKR section. |
| Implementation tasks | `writing-plans` only after Language, OKR, and Design are approved. Its header and tasks live under Implementation plan in the same `plan.md`; no separate plan file, commit, execution offer, or implementation skill. |
| Mockup | `codebase-design` and its `DESIGN-IT-TWICE.md` only after completion gate passes. |

Implementation-task commit steps describe future atomic commits on the temporary
branch; `implement-prepared-plan` merges them without squashing. Record this in
Global Constraints. Never execute those commits while planning.
If independent subsystems require a scope decision, ask within this plan before
splitting draft jobs. Do not open another plan folder.

Use one grilling frontier round for reuse/adapt/skip when a similar implementation
was found. Otherwise ask one brainstorming question per message. Questions
whose answers depend on an open answer wait for the next round. Apply these
same interview rules to `okr-strategist` instead of its up-to-five-question batch.
If the user skips questions, state and record assumptions in OKR; skipping
questions does not automatically approve Language, OKR, or Design.
