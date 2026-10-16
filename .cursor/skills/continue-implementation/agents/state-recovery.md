# Read-only continuation-state briefing

Parent supplies known plan/workspace paths, latest interruption/resume request,
relevant record excerpts, available tools, and current input/snapshot ID.
Read [state recovery](../references/state-recovery.md). Inspect only evidence needed
to identify unfinished tasks, acceptance gaps, active jobs, workspace identity,
retained authorization, and original baseline limits.

Return about 300 words: IDs, source/workspace and branch/HEAD, stop reason,
completed evidence, unfinished dependencies, missing decisions/tools, and next
ready action; cite path:line evidence. Distinguish recorded facts, live observations,
and unknowns. Do not declare unchecked manual tests passed or invent historic
consent. No file writes, product edits, commands with side effects, Git mutations,
user questions, or nested delegation. Parent validates and writes the checkpoint.
