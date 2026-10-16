# Continue the authorized phase

Use `implement-prepared-plan` as the existing workflow, entering its appropriate
phase rather than invoking a fresh whole-run preparation. Read the actual installed
phase references before using them. Its no-push/no-PR/no-squash, baseline preservation,
authorization, single-parent Git, and final gate rules remain in force.

Recover task dependencies and checklist ownership. Schedule unfinished ready tasks;
for a completed task missing evidence, verify it rather than reimplementing it.
For a review defect, repair the affected slice and repeat affected checks. For an
interrupted merge, inspect actual Git state first; do not blindly repeat the merge.
If only final cleanup/reporting remains, resume it without another implementation
cycle, removing only owned resources with all wanted content safely retained.

## Cursor and focused discovery

Use the exposed Cursor Task/mode/workspace tools. If still in Plan mode, resume
editing only after retained start/workspace authorization is established; request
the actual editing-mode switch only if the session requires it. Never invoke a
fictional tool or change the agreed branch strategy to get around a missing tool.

For unknown code facts, use the implementation skill's Graphify MCP-first discovery:
actual query_graph/get_node/get_neighbors schemas, correct absolute project_path
when supported, bounded results, and verified current-workspace evidence. Do not
require local graph files for MCP access or treat a stale graph as current code.
Use recorded still-valid facts; local graph/wiki/source fallbacks stay available.
No reindex, installation, or MCP configuration change simply to resume.

## Small parallel jobs

Parent owns approvals, current checkpoint, artifact writes, and all Git mutations.
Use bounded Task jobs with task/snapshot ID, absolute workspace, relevant excerpts,
one question/output, evidence paths, file allowlist, dependencies, and stop condition.
Reuse implement-prepared-plan's implementer, task-check, and review templates.
Read-only recovery/check workers never write records; implementers edit exclusively
assigned product files and do not stage/commit or change shared plan artifacts.

Parallelize independent fact checks, stable snapshot reviews, or implementation
slices only with disjoint files/resources and settled interfaces. Normally use at
most two workers. A running test or manual-test dependency cannot be made
independent by relabeling it. No overlapping writers, concurrent Git mutations,
or recursive delegation. Without Task, use a recorded sequential fallback and
separate verification pass instead of claiming subagent independence.

## Evidence, review, and integration

Log new results in the existing records; retain evidence still valid for current
scope/code. Clear false done marks and invalidate only results affected by edits
or stale snapshots. Refresh end SHA and include attributable staged, unstaged,
and untracked implementation changes in review; preserve original start/baseline.
Use the original independent acceptance checks and Standards/Spec reviews, scoped
to unfinished or changed work. Known unchanged checks need not be run repeatedly.

When all required gates actually pass, finish the previously authorized non-squash
integration and safe cleanup under the original Git contract. Otherwise keep the
workspace intact and report pending verification, external blocker, or missing
authorization precisely. Never silently mark a manual gate optional to merge.
