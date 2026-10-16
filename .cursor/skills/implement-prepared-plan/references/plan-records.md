# Source plan and implementation records

Use the existing `.ai/plans/NNN-short-description/plan.md` selected by the user.
If unspecified, identify the active prepared plan; ask when multiple candidates
remain plausible rather than choosing an arbitrary newest folder. If missing,
stop. Keep a legacy folder containing `þlans` as it stands. Never allocate a new
number, rename the folder, or duplicate the plan for this implementation.

Resolve the actual repository affected by the plan with `git rev-parse --show-toplevel`.
Record its absolute checkout/plan paths, branch, HEAD, and current dirty state
before writing implementation records. Check Language, OKR, Design, and task
approval state. An unfinished prepared plan or unresolved scope is a preparation
gap, not permission to design/implement it silently. For multiple repositories,
record each baseline and integration boundary; do not imply one repository's
merge also integrates another. Clarify coordination if the plan did not settle it.

The main agent is the sole writer of these records in the existing folder:

| File | Purpose |
| --- | --- |
| `plan.md` | Source from prepare-plan. Preserve Task, Log, Decisions, Glossary, OKR, Design, and Implementation plan. Append `## Adjustment` only for an accepted clarification that changes it. |
| `checklist.md` | Acceptance items and their evidence-backed status; separate from tasks. |
| `tasks.md` | Ordered task IDs, dependencies, exclusive files, checklist ownership, checks, and completion evidence. |
| `context.md` | Settled dictionary, paths, project rules, baseline state, and facts implementers need; no duplicated task list. |
| `plan.refactored.md` | Read-only refactor analysis; alternative proposal, never the source unless the user explicitly adopts it. |
| `suggestions.md` | User suggestions and clarification answers; create only upon the first suggestion. |
| `review-range.md` | Recorded checkout/branch, start and refreshed end SHAs, baseline attribution, snapshot IDs, reviewed committed and uncommitted plan paths, and limits. |
| `wayfinder.md` | Compact local phase/decision/job map when used; do not open an issue tracker. |
| `bugs.md` | Confirmed bug evidence when a defect is found; do not create empty scaffolding. |

Give each task a stable ID and associate worker results with an input/snapshot
revision. Preserve historical decisions and record approval/branch choice so
continuation does not repeat questions. During worktree execution, use the copy
of this same folder in the agreed workspace and its absolute paths; do not
maintain competing authoritative copies. Include implementation records in the
approved integration. On the recorded branch, commit only with explicit consent.
