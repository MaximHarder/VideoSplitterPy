# Recover the existing run

## Find the source and workspace

Use the user-specified plan/workspace, current session evidence, or existing
implementation records. Read relevant sections of plan.md, tasks.md, checklist.md,
context.md, review-range.md, and wayfinder.md when present; inspect suggestions.md,
bugs.md, or plan.refactored.md only if relevant. Missing optional records are not
a reason to create empty files or restart preparation. If multiple runs remain
plausible, ask which one; do not guess the newest folder. If no prepared source
exists, explain the missing source and stop dependent implementation.

Load the installed `implement-prepared-plan` via Cursor's skill catalog or its
sibling directory. It remains the execution/Git authority; use its existing
source-plan, delegation, execution, verification, and integration rules at the
phase that needs them. Do not silently adopt plan.refactored.md or redesign scope.
If the dependency is unavailable, recover/report state read-only and identify the
missing dependency before executing its workflow.

Read current repository root, branch, HEAD, worktree list, staged/unstaged changes,
and untracked paths. Confirm the actual agreed implementation workspace, especially
when records were written in its plan-folder copy. Do not switch branches merely
to match an old record. Changed/deleted worktrees or unexpected branches require
reconciliation before dependent edits, not automatic recreation or merge.

## Protect historical evidence

Retain the original recorded checkout, branch, start SHA, dirty baseline, and
accepted adjustments. Do not replace start with current HEAD or infer missing
historical dirty attribution from today's diff. Preserve current data before
updating records, including user edits to those records. A fresh protective
snapshot is today's state, not the original baseline. Missing attribution blocks
unsafe staging/merge, not independent read-only verification. Resume edits only
after reconciling the actual workspace, preserving its current content, and
establishing ownership for the assigned paths; defer edits whose safety depends
on unknown historical changes. A fresh snapshot never resolves historical
attribution for committing or integration.

Find recorded start, workspace/branch, commit, and integration authorization.
Reuse explicit answers from records or session; do not re-ask them. An explicit
user request to resume approved implementation authorizes continuation of that
work; it does not settle an absent branch preference or commit/integration choice.
Ask only for a genuinely missing decision before its dependent operation. If the
user explicitly paused the run, a new resume request lifts that pause; do not
interpret unrelated status questions as resume authorization.

Check whether a command or subagent is still running before relaunching its work.
Use session/job state when available; do not duplicate a migration, test with
side effects, or active writer. Reconcile/cancel obsolete workers through the
available tools before assigning overlapping files. Do not kill unrelated processes.
Do not trust stale done marks or worker claims without actual diff/check evidence.

## Compact checkpoint

The parent adds a dated Continuation section to the existing context.md (or
wayfinder.md index), preserving earlier content. Include:

- source and absolute workspace; current and recorded branch/HEAD;
- carried-forward approvals and material missing decisions;
- completed tasks with usable evidence; unfinished task/check IDs;
- stop reason, current blocker status, and next dependency-ready action;
- current input/snapshot ID, active jobs/file ownership, and pending manual checks;
- exact command/procedure and external input needed for any remaining blocker.

Do not create a new plan number, copy logs wholesale, or invent past evidence.
Update this checkpoint before any final handoff so another invocation can resume.
Use [the recovery briefing](../agents/state-recovery.md) when inspection would
otherwise consume substantial main context; known simple facts can stay inline.
