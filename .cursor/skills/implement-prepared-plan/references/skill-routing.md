# Load skills at their phase

Discover available skills through [Cursor runtime](cursor-runtime.md). Read each
before using it and announce meaningful switches. Do not load all skills at startup.

| Phase | Skills |
| --- | --- |
| Breakdown/delegation | `create-subagent` for bounded briefs; context skills only for their operations. |
| Clarification | `grill-with-docs`, then its required `grilling` and `domain-modeling`. Workers return proposed terms/questions; parent handles interview and writes. |
| Analysis | Read-only `refactor-plan`, written by parent to plan.refactored.md. Its review request is consolidated with the start gate; alternate source requires adoption. Task analysis is bundled in this skill. |
| Workspace | `using-git-worktrees` only for approved isolation; `git-workflow-and-versioning` for authorized atomic commits and non-squash merge. Mandated Git tooling takes precedence over generic CLI examples. |
| Execution | `subagent-driven-development` for independent tasks, `executing-plans` for coupled tasks; language/project skills before edits, per [project rules](project-rules.md). Worker Git/artifact ownership is overridden by [delegation](delegation.md). |
| Review | `code-review` for parallel Standards/Spec, `caveman-review` for concise findings, applicable read-only bug investigation. |

No push, PR, squash, or `finishing-a-development-branch`, regardless of supporting
skill suggestions. Do not follow a generic reset/clean/stash example that destroys
user work. Use existing authorization instead of repeated routine consent requests.
Missing required skills pause only dependent work with an exact explanation;
independent preparation may proceed. Do not claim to have followed missing skills.
