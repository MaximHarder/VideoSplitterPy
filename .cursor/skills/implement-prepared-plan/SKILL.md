---
name: implement-prepared-plan
description: >-
  Implement an existing prepare-plan plan.md with preparation, explicit start
  and workspace authorization, bounded task delegation, evidence-backed checks,
  and final review. Preserve existing dirty work; use atomic commits and a
  non-squash merge when a temporary branch is approved. Use only when explicitly
  invoked. Does not push or open pull requests.
disable-model-invocation: true
---

# Implement a prepared plan

`plan.md` is the source. Do not redesign it or start another plan folder.
Reply in the user's language. No product code, branch, or worktree creation
before the authorization gate. Never push, open a PR, squash, or discard user work.
The main agent owns approvals, plan artifacts, scheduling, and Git mutations.
Implementers may edit only assigned product files in the agreed workspace.

## Execution order

Resolve links relative to this skill folder. Read references and supporting
skills only when their phase needs them. This order and its ownership rules
resolve conflicting sequencing in supporting skills.

| Phase | Main agent | Delegated work | Exit condition |
| --- | --- | --- | --- |
| 0. Resolve source | Read [runtime](references/cursor-runtime.md), [plan records](references/plan-records.md), and [Git contract](references/git-workspace.md). Locate the existing plan and record repository, branch, start SHA, and dirty baseline. | None needed for known paths. | Source exists; plan status and approval gaps known; baseline recorded. |
| 1. Prepare tasks | Read [preparation](references/preparation.md), [delegation](references/delegation.md), and [skill routing](references/skill-routing.md). Save checklist and tasks in the existing folder. | [Breakdown](agents/task-breakdown.md); then [clarification](agents/task-clarification.md). Graph-first fact lookups for unknowns. | Revised tasks, checklist, and context written by parent. |
| 2. Analyze | Apply [task analysis](references/task-analysis.md) to the clarified snapshot. Integrate scope-preserving fixes; investigate and write plan.refactored.md. | [Task analysis](agents/task-analysis.md). Independent graph-oriented code facts may run beside coverage analysis. | Material conflicts resolved; refactor analysis saved; adoption remains optional; no product code. |
| 3. Authorize | Follow [start and suggestions](references/start-and-suggestions.md). Resolve suggestions, start approval, and temporary-branch preference; reuse prior explicit answers. | Read-only fact clarification as needed. | Start and branch choice explicit; alternate source adopted only if expressly requested. |
| 4. Establish workspace | Follow [Git contract](references/git-workspace.md), then load [project rules](references/project-rules.md) and applicable execution skills. | Bounded baseline checks if independent. | Agreed workspace and baseline verified; no silent switch to another branch strategy. |
| 5. Implement | Follow [execution](references/execution.md); schedule dependency-ready tasks with exclusive files. | [Implementer](agents/task-implementer.md); [independent check](agents/task-check.md) after each completed slice. | Each slice has evidence-backed acceptance and authorized serial commit, or remains uncommitted by choice. |
| 6. Review | Follow [verification](references/verification.md). Refresh end SHA and review snapshot; resolve gaps without restarting approvals. | [Review](agents/final-review.md): Standards and Spec in parallel; focused read-only bug investigation as applicable. | All checklist items done or explicitly out of scope; final review gaps resolved. |
| 7. Integrate | Follow [Git contract](references/git-workspace.md) only after final gate passes. Merge without squash if approved; safely remove owned temporary resources. | None; Git integration is serial parent work. | Work integrated or safely retained with a precise blocker report; no push. |

## Context and revisions

Keep only phase, open decisions, task IDs, ownership, evidence pointers, and short
results in the main chat. Use [delegation](references/delegation.md) for bounded
briefs and parallelism. New scope invalidates affected tasks/checks; clarify and
resume their earliest affected phase. Do not repeat unchanged start/branch consent.
`agents/` contains prompt templates explicitly read for Cursor Task calls, not
registered custom subagents. `agents/openai.yaml` is optional metadata for other
hosts; Cursor's explicit-only setting remains in this file's frontmatter.
