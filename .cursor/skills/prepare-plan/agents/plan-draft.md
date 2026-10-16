# Implementation-task drafting briefing

Parent supplies snapshot ID, approved Language/OKR/Design excerpts, frozen
interfaces/global constraints, relevant evidence paths, and exactly one task
group with its assigned task and commit order. Read `writing-plans` through the
actual skills catalog and [the plan contract](../references/plan-file.md).

Return only the assigned implementation-task text for insertion into plan.md.
Include exact files/interfaces, failing tests, minimal implementation guidance,
verification commands and expected output, and future atomic commit steps.
Respect approved paths, language, success criteria, and neighboring interfaces.
Do not invent unknown APIs or test commands: return a dependency/unknown to the
parent if it prevents a usable draft. Do not silently broaden scope.

No file writes, implementation, executed commits, user questions, or recursive
delegation. Return snapshot ID and assumptions with the proposed section.
The parent integrates and self-reviews it; a worker draft is not approval.
