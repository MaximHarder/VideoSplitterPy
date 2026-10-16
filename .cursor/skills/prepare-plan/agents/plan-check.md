# Read-only plan-check briefing

Parent supplies one focus (`coverage` or `feasibility`), snapshot ID, absolute
plan/project paths, approved decisions, and relevant evidence. Review exactly
that completed plan snapshot. Follow [the compact result contract](../references/context-management.md).

Coverage: check each task against approved scope, Design, and OKR; missing
requirements, contradictions, placeholders, and unauthorized additions.
Feasibility: check Language/Tech Stack/path consistency, referenced interfaces,
task dependencies, verification commands/expected output, and future atomic
commit order. Use read-only evidence; do not implement or execute plan steps.

Return snapshot ID, findings with plan and repository path:line evidence,
severity, and suggested corrections, or no findings with material limits.
No file writes, user questions, changed approvals, or recursive delegation.
The parent resolves findings and performs `writing-plans` self-review.
