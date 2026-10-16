# Prepare before product code

## 1. Breakdown

Read the source plan and delegate [breakdown](../agents/task-breakdown.md).
Return an acceptance checklist and ordered task list with stable IDs, dependency
edges, paths, and owned checklist items. The parent writes `checklist.md` and
`tasks.md` in the existing folder before clarification begins. Do not change
scope, create a separate source plan, or register a permanent agent.

## 2. Clarify against the plan

Use [clarification](../agents/task-clarification.md) as a separate read-only job
with `grill-with-docs`, `grilling`, and `domain-modeling` when available. The job
settles terms from evidence, identifies questions the plan already answered,
and proposes revised tasks and context. The parent integrates those tasks and
writes `context.md`. Workers do not ask the user or assume missing decisions.
Use graph-first discovery for facts the repository can provide. Ask the user
only for material choices the source and evidence do not settle.

## 3. Analyze coverage and feasibility

Run [task analysis](task-analysis.md) after the revised tasks/context exist.
This check depends on clarification; do not launch both against different task
versions. Independent evidence lookup for unknown code facts may run beside
coverage analysis, then join results before applying fixes. Apply HIGH/MEDIUM
recommendations that preserve approved scope without asking for routine edits;
clarify any recommendation that changes behavior, outcomes, or authorization.
Material CRITICAL conflicts block dependent implementation; do not drop them.

## 4. Refactor analysis

Read `refactor-plan`, investigate the touched code read-only, and write its
analysis to `plan.refactored.md`. A bounded investigator may gather code facts;
the parent writes the analysis. Do not edit product code or replace plan.md.
This skill overrides only the output location and consolidates its review gate
with [the start gate](start-and-suggestions.md). The proposal is an alternative,
not authorization for a refactor or a new implementation source. If the user
adopts it, append the accepted adjustment and regenerate affected tasks/checks.

Proceed to start/branch authorization only after checklist, revised tasks,
context, resolved material analysis, and plan.refactored.md are present.
