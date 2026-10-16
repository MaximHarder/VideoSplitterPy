---
name: prepare-plan
description: >-
  Plan one user task in Cursor Plan mode through memory-backed interviews,
  confirmed language and design, OKRs, an implementation plan, and a module
  mockup. Record the workflow in .ai/plans/NNN-short-description/plan.md.
  Use only when the user invokes prepare-plan or /prepare-plan. Does not implement.
disable-model-invocation: true
---

# Prepare plan

Plan one task in Cursor Plan mode. Do not implement, scaffold, or commit.
Reply in the user's language. Keep identifiers and skill names unchanged.
Only the main agent writes `plan.md`, `wayfinder.md`, and `design-mockup.md`
inside one active `.ai/plans/NNN-short-description/` folder.
Implementation is a separate request via `implement-prepared-plan`.

## Execution order

Resolve links relative to this skill folder. Load references and supporting
skills at their phase, not all at startup. The sequence below governs conflicts
about ordering in supporting skills. Never pass a gate on an unconfirmed assumption.

| Phase | Main agent | Delegated work | Exit condition |
| --- | --- | --- | --- |
| 0. Enter planning | Read [runtime](references/cursor-runtime.md), then [skill routing](references/skill-orchestration.md). Read `using-superpowers`; enter or verify Plan mode. | None before Plan mode. | Plan mode active; rejection stops the workflow. |
| 1. Create record | Read [plan file](references/plan-file.md) and [delegation](references/context-management.md). Create the next free plan folder and log the raw task. | None before the record exists. | Absolute plan path and current input ID established. |
| 2. Gather evidence | Follow [memory search](references/memory-search.md). Merge compact results into the input log. | Graph orientation first; then connected-memory search and repository facts in parallel when useful. | Current evidence collected; unavailable sources distinguished from no hits. |
| 3. Settle decisions | Follow [interview](references/interview.md) and [language rules](references/plan-mode-and-language.md): scope/reuse → approach and Language → OKR → Design. Ask, log, and wait at each approval. | Read-only fact lookups for open questions. | Language, OKR, and Design confirmed; decision frontier empty. |
| 4. Draft tasks | Read `writing-plans`; freeze approved interfaces and constraints. Integrate drafts under Implementation plan in `plan.md`. | [Task drafting](agents/plan-draft.md), parallel only for independent groups with settled boundaries. | Complete integrated draft matching the approved decisions. |
| 5. Validate plan | Run `writing-plans` self-review and reconcile findings. | [Plan checks](agents/plan-check.md): coverage and feasibility on the same frozen draft, in parallel. | Completion gate in [completion](references/completion-and-mockup.md) passes. |
| 6. Mock up modules | Read `codebase-design` and `DESIGN-IT-TWICE.md`; compare alternatives and write `design-mockup.md`. | [Interface alternatives](agents/interface-review.md) in parallel; optional available Grok second opinion. | Mockup agrees with approved plan; any changed decision reapproved. |
| 7. Final review | Present `plan.md` and `design-mockup.md`; ask for final changes. | None unless a requested change needs new evidence. | User finishes planning; no automatic implementation or mode change. |

## Every new user input

Log it before replying. Run phase 2 before the next interview question; reuse
valid repository facts and only refresh facts affected by the input. Resume the
earliest affected phase instead of restarting or opening another plan folder.
An input changing an approved decision invalidates dependent drafts/checks:
reconfirm that decision and repeat only the affected downstream work.

## Context discipline

The main chat holds the phase, open decisions, evidence paths, and short results.
Delegate independent read-only lookups, drafts, and checks under the
[delegation contract](references/context-management.md). Keep user questions,
approvals, orchestration, and final artifact writes in the main agent.
`agents/` contains explicitly loaded prompt templates; these are not registered
Cursor subagents. `agents/openai.yaml` is optional metadata for other hosts;
Cursor's explicit-only policy is in this file's frontmatter.
