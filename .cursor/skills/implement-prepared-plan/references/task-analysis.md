# Task analysis

This is the `speckit-analyze` template, aimed at this skill's files. The check subagent follows it. It does not run `.specify/scripts/bash/check-prerequisites.sh`. It does not require `spec.md`. The parent, not the subagent, writes scope-preserving HIGH and MEDIUM fixes into `tasks.md`. Conflicts changing approved scope require clarification.

**Read-only for the subagent.** It returns a report. It does not edit files.

**Constitution.** If `{project folder}/.specify/memory/constitution.md` exists, load it. A conflict with a MUST principle is CRITICAL. Do not weaken the principle. If the file is absent, say so and continue. Do not invent principles.

**Load only what the check needs.**

- Prepared plan: decisions, constraints, files, and success checks.
- `checklist.md`: items that must be true when the work is done.
- `tasks.md`: task ids, descriptions, order, and file paths.
- `context.md`, if it already exists: terms and paths. Do not treat a missing `context.md` as a failed check.

**Models, kept inside the report.**

- Each plan decision that needs a task.
- Each checklist item.
- Which task covers which decision or checklist item.

**Detection.** At most 50 findings. Summarize the rest.

- Duplication: two tasks or decisions that say the same thing. Keep the clearer one.
- Ambiguity: words like fast, safe, simple, or robust with no check; leftover TODO, `???`, or `<placeholder>`.
- Underspecification: a task with no file or no outcome; a checklist item with no task.
- Constitution: a MUST conflict, or a required gate the plan dropped.
- Coverage: a plan decision or checklist item with no task; a task that matches nothing in the plan.
- Inconsistency: one thing named two ways; a task ordered before the task it depends on; two decisions that cannot both be true.

**Severity.**

- **CRITICAL**: constitution MUST conflict, or a missing task that blocks the plan from working.
- **HIGH**: duplicate or conflicting decision, an untestable check, a security or data rule with no measurable outcome.
- **MEDIUM**: two names for one thing, a missing edge case, a checklist item with a weak task.
- **LOW**: wording, or a repeat that does not change the order.

**Report.** No file write. One row per finding.

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|

Then: coverage table (decision or checklist item, has task, task ids), constitution issues, tasks with no decision, and counts for decisions, tasks, coverage, ambiguity, duplication, and critical issues.

The subagent does not ask the user to apply fixes. The parent applies scope-preserving HIGH and MEDIUM recommendations without asking. Do not silently expand scope. A CRITICAL constitution or plan conflict stays recorded and blocks dependent work until resolved with the user; preserving plan.md does not justify dropping the finding.


Use [the analysis briefing](../agents/task-analysis.md). Associate the report with
the clarified snapshot. Keep the original limit of 50 findings in a bounded report,
but return a compact summary and evidence locations first; no raw tool transcripts.
A missing constitution is a reported absence, not an invented failure.
