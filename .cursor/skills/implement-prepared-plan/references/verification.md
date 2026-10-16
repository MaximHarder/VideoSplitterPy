# Independent acceptance checks and final review

## Per-task checker

Give a fresh [checker](../agents/task-check.md) task/snapshot ID, checklist items
it owns, actual attributable diff, baseline facts, and acceptance commands/results.
Its job is to judge evidence independently, not edit files. The parent writes its
status into checklist.md/tasks.md, preserving evidence and unchecked gaps.

- **done**: each owned item's requested outcome is demonstrated by path:line diff
  evidence or a named command/result. Record that evidence before checking it.
- **not done**: missing or partial outcome. Clear a previous done mark and name
  the gap. The parent cannot override this by ticking it without new evidence.
- **not this task**: later/other task ownership; keep it open and correct a false
  mark assigned to this task.

A checkbox is not evidence. Do not mark the task complete while any owned item
is not done. Fix gaps and recheck; block dependent tasks, not independent work.
Without Task, perform a separate explicit verification pass and record the reduced
independence. Do not claim a subagent review occurred.

## Final stable snapshot

Join all workers, finish checks, and freeze a completed implementation snapshot.
Refresh end in review-range.md to current HEAD, not only when empty. Include
uncommitted staged/unstaged/untracked plan changes and baseline attribution.
Use `code-review`: Standards and Spec in parallel, spec is plan.md plus accepted
Adjustments (or an explicitly adopted alternate). Use its review template even
when docs/agents/issue-tracker.md is missing. Use `caveman-review` to report concise
findings; a `cavecrew-reviewer` may read the diff when appropriate, but do not
commission a duplicate review merely for formatting.

Run focused read-only changed-behavior bug investigation when meaningful or
required by the plan, using an applicable `find-bugs` or repository equivalent.
Do not use a repository-specific skill outside its stated scope.
Run required acceptance, build, lint, type, or test commands appropriate to the
change. Distinguish existing baseline failures from introduced failures and
report limits; do not describe unrun checks as passed.

Review gaps return to the affected task and its evidence checks. A changed
snapshot invalidates relevant reviews; update end and rerun affected checks.
Do not restart breakdown, create another folder, or repeat existing branch/start
approval unless the fix changes authorized scope/workspace choice.

The final gate passes only when every checklist item is done with evidence or
explicitly out of scope in the approved plan, required checks are resolved, and
reviews have no open material gap. Only then may the parent integrate under
[the Git contract](git-workspace.md). Report what changed, evidence, branch state,
and concrete remaining limits. No push or PR.
