# Bounded implementation briefing

Parent supplies one approved task ID/snapshot, absolute agreed workspace, exclusive
file allowlist, plan/context excerpts, dependencies already passed, relevant project
rules/skills, acceptance items, baseline facts, and verification commands.
Follow [execution](../references/execution.md) and [ownership](../references/delegation.md).
Implement only this slice, loading its applicable language/project skills before
editing. Run assigned checks that do not mutate another worker's resources.
If a required change escapes the allowlist or scope, stop and return the dependency
for parent reassignment; do not touch shared files or another worker's changes.
Return IDs, changed paths, command results, limitations, and acceptance gaps.
No plan-artifact writes, Git mutations, user questions, or recursive delegation.
The parent commits after independent acceptance checks when authorized.
