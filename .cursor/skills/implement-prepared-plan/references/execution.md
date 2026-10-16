# Execute dependency-ready tasks

Start only after preparation and start/workspace gates pass. Use the revised
tasks.md and the agreed source plan, with accepted adjustments. Read applicable
language/project skills before editing, per [project rules](project-rules.md).

Use `subagent-driven-development` when tasks are mostly independent and Task is
available; use `executing-plans` for tightly coupled tasks or sequential execution.
Override any worker commit/artifact writes with [the delegation contract](delegation.md).
Do not pause between already-authorized tasks. Workers get a fresh bounded task
brief; assign disjoint files for parallel edits. Shared interfaces, migrations,
generated resources, and lockfiles require serial ownership.

After each completed task, use an independent [task checker](../agents/task-check.md)
against the stable actual diff and owned acceptance items. The parent records
its results in checklist/tasks and commits only authorized validated slices.
A failed check blocks that task's dependents; unrelated ready tasks may continue.
Fix the gap and recheck it without replaying the entire preparation/approval flow.

If a real ambiguity changes behavior or approved scope, stop its dependent work,
use `grill-with-docs` and its required skills to clarify, and wait. Do not guess.
When a defect is reported/discovered, use read-only evidence-led investigation
before fixing the responsible code. Use `find-bugs` only when its installed scope
covers this repository; otherwise apply the repository's appropriate investigation
workflow. Delegate `bug_finder` when available. Record confirmed evidence in bugs.md.
The investigation does not itself authorize unrelated fixes.
