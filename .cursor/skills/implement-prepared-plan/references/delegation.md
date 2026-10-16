# Bounded delegation and parallel ownership

## Parent and worker roles

Parent owns user questions/approvals, phase state, shared plan artifacts, task
scheduling, integration, and ALL Git mutations. Workers never stage, commit,
switch/create branches, merge, stash, reset, push, or register persistent agents.
No nested delegation unless explicitly assigned by the parent.

Read-only workers: breakdown, clarification, analysis, discovery, task checks,
reviews, and bug investigation. They return proposals/evidence, never file edits.
Implementers: one approved task, exclusive product-file allowlist, agreed absolute
workspace path. They may edit only that allowlist and run assigned verification
commands. No shared checklist/task/context edits. Unexpected required shared-file
changes return to the parent for reassignment or serial execution.

## Parallel eligibility

Normally use at most two workers concurrently, respecting the session limit.
Parallelize only jobs with available inputs and no dependency edge. Clarification
waits for breakdown; task analysis waits for clarified tasks; task checks wait for
completed slices; final review waits for all implementation workers. Independent
Graphify-oriented fact lookup may run beside a read-only coverage check.

Implementers may run together only with disjoint file ownership, settled interfaces,
and commands that do not mutate shared generated files, services, databases, or
build resources. Shared file/lockfile/schema/migration jobs and Git run serially.
Checks of completed disjoint slices may overlap other disjoint work only when
reviewed files and relevant test resources remain stable. Otherwise join workers
and freeze the snapshot first. Never let a review certify a moving target.

Assign task/commit order before launch. Join each dependent batch, validate evidence,
and release file ownership before reassigning it. Commit validated slices serially
in plan order, only with existing authorization. A failed task blocks dependents;
independent ready jobs may continue. Cancel/invalidate stale jobs after new scope
or input changes; rerun only affected work.

## Brief and output

Pass one job, task/snapshot ID, exact scope, absolute workspace/plan paths, source
section excerpts, accepted decisions, relevant evidence, dependencies, file ownership,
tool permissions, expected checks, output shape, and stop condition. Pass paths
rather than the full chat or growing logs. Worker reads its template and only
applicable references/skills. `create-subagent` supplies briefing shape when available;
do not install templates as `.cursor/agents/` files.

Evidence/check results: about 300 words, status (`done`, `blocked`, `no-hit`,
`unavailable`, or `needs-clarification`), IDs, path:line facts/findings, check results,
uncertainties, and next dependency. Drafts may return the complete assigned artifact
text needed for integration; no full source dumps or tool transcripts. Implementers
return changed paths, test results, limitations, and remaining acceptance gaps.

Use `wayfinder` as a compact local index: phase, task/job IDs, open decisions,
ownership, and evidence pointers. No issue tracker or duplicate ticket transcripts.
Use `cavecrew-investigator` for locations, `cavecrew-builder` for known one/two-file
patches, and `cavecrew-reviewer` for findings when available. Larger implementation
slices need an ordinary implementation agent or main execution, not that builder.
Use clear compressed `caveman` briefs; user-facing language stays normal.
Shorten briefs in memory. `caveman-compress` must never overwrite source plans,
implementation records, or skill files; do not add scratch artifacts just to use it.

If Task is unavailable, execute sequentially in the main context with recorded
fallback and a separate verification pass; never invent worker execution or evidence.
