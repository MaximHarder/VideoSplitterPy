---
name: continue-implementation
description: >-
  Resume an existing implement-prepared-plan run after manual-test handoff,
  failed checks, unavailable tools, session interruption, or another blocker.
  Recover the same plan, workspace, approvals, and evidence; continue unfinished
  authorized tasks without restarting preparation. Not for starting a new plan.
---

# Continue implementation

Resume the existing implementation, not a new plan or branch. Reply in the user's
language. Retain accepted scope, source plan, workspace choice, and prior approvals.
Never treat invocation as a manual-test pass, acceptance waiver, or new permission
to push, open a PR, squash, discard work, or change the branch strategy.

## Resume sequence

1. Read [state recovery](references/state-recovery.md). Locate the active plan
   and actual workspace; inspect current files, Git state, approvals, unfinished
   jobs, and stop reason. Recover a compact checkpoint before any edits.
2. Classify the interruption using [verification and blockers](references/verification-and-blockers.md).
   Confirm whether an old blocker still exists. Automate a manual check with
   available suitable tools when possible; keep genuinely unavailable checks
   pending and continue independent authorized work.
3. Read [continuation and delegation](references/continuation.md). Resume the
   earliest unfinished dependency-ready task or review in `implement-prepared-plan`.
   Load only that skill's phase-specific references. Do not rerun its entire
   preparation/start sequence or ask for unchanged approvals again.
4. Independently check repaired/completed slices, update the existing records,
   refresh review snapshots, and repeat only checks affected by new code or evidence.
   Pending required acceptance remains pending; do not mark it passed or drop it.
5. Integrate only when the original final gate and integration authorization
   actually pass. Otherwise retain the workspace safely and report the exact
   remaining blocker and next action in the checkpoint.

The parent owns shared records, questions, and Git mutations. Delegated jobs use
bounded briefs and exclusive ownership, with parallel independent jobs when useful.
[The recovery briefing](agents/state-recovery.md) is an explicitly loaded Cursor
Task template, not a registered custom subagent. Automatic discovery is allowed;
selection of this skill does not itself authorize mutations beyond the request.
