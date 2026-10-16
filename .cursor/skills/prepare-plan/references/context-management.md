# Delegation and context contract

## Ownership

The main agent owns phase transitions, user questions, approval state, the active
plan path, and all artifact writes. Subagents are read-only: they return evidence,
proposed text, or findings. They never edit shared files, create another plan,
ask the user questions, change modes, implement, scaffold, or commit.

Use Cursor Task when available; follow [runtime](cursor-runtime.md) otherwise.
Prefer independent small jobs with bounded output. Do trivial known facts inline;
do not spawn an agent just to format one line. Parallelize when jobs have all
inputs and neither needs the other's result. Respect the runtime's concurrency
limit; normally use at most two workers at once and queue extra jobs rather
than launching nested agent trees.

## Jobs and dependency barriers

| Job | Inputs required | Parallel with | Template |
| --- | --- | --- | --- |
| Graph orientation | Logged current input, project root | No repository scout until orientation returns or graph unavailability is recorded | [Memory](../agents/memory-search.md), orientation stage |
| Connected-memory search | Orientation result, current input | Repository scout | [Memory](../agents/memory-search.md), connected-memory stage |
| Repository scout | Orientation result, specific unknown facts | Connected-memory search or another disjoint fact lookup | [Repository facts](../agents/repository-scout.md) |
| Implementation task draft | Approved Language/OKR/Design; frozen interfaces and global constraints | Drafts for independent groups only; assign task/commit order before launch | [Task draft](../agents/plan-draft.md) |
| Coverage / feasibility checks | Same completed draft snapshot | Each other | [Plan check](../agents/plan-check.md), one focus per job |
| Interface alternative | Completion gate passed; one selected alternative | Other alternatives; available Grok review | [Interface](../agents/interface-review.md) |

Never run a draft before its decisions are approved, a review before its draft
exists, or a mockup before plan validation passes. If a draft group consumes
another group's interface, settle that boundary first or draft serially.
After editing a reviewed snapshot, repeat only checks affected by the edits.

## Brief and result

Give each agent one job, input/snapshot ID, absolute project and plan paths,
the original task, current question/answer context, relevant section excerpts,
approved constraints, previous useful hits, evidence paths, tools it may
use, output shape, and stop condition. Pass file paths rather than the entire
chat or skill collection. The agent reads only its template and task-relevant
references/skills. Use compressed clear briefs (`caveman`) without omitting
constraints. No recursive delegation unless the parent explicitly assigns it.

Evidence/check jobs return at most about 300 words: status (`found`, `no-hit`,
`unavailable`, `blocked`, or `done`), input/snapshot ID, path:line evidence,
findings, uncertainties, and the next required dependency. Draft jobs return
only their assigned section plus a short list of assumptions; complete task
instructions must not be shortened into an unusable plan. Do not return tool
transcripts, full source files, or unrelated advice.

Join a parallel batch before using its findings for the next question or gate.
Check paths and material claims, deduplicate results, reject stale input IDs,
and log useful evidence and decisions. If new input changes the job's basis,
cancel or invalidate that job; unaffected results can remain valid.

## Local decision map

Use `wayfinder` for `wayfinder.md`: Destination, Notes, Decisions so far,
Not yet specified, Out of scope. Add the current phase, input/snapshot ID, job
status, and evidence pointers under Notes. This is a compact resume index;
`plan.md` remains the record of user messages and accepted decisions.
Do not open an issue tracker or store duplicate transcripts in the map.

Use `cavecrew-investigator` for code locations and `cavecrew-reviewer` for
findings when those presets exist. The supplied templates remain usable without
those presets. Do not use `cavecrew-builder` to implement during planning.
Load context skills only when performing their respective operation.
Shorten large briefs in memory. Do not invoke `caveman-compress` while its
overwrite/copy operation would require files outside the three permitted
planning artifacts; never run it on plan artifacts or skill files.
