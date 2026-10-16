## One plan file

Project folder is `git rev-parse --show-toplevel`. If that fails, use the workspace root.

```text
{project folder}/.ai/plans/{version_id}-{short-description}/plan.md
```

- `{version_id}` is three digits. List `.ai/plans/` and take the next free `NNN-` directory. The first plan is `001`.
- `{short-description}` is a short kebab-case name of this task. No number in the slug.
- Do not reuse an existing folder. Do not open a second plan while this one is active.
- Create the file immediately, before the memory search, and put the user's raw task in it.

If a later message is a different task, ask once whether it belongs in this plan. Until the user says otherwise, append it here. Do not start `002` while this plan is active.

The main agent is the only writer. Append every user message verbatim, useful
search finding, unavailable source, question, answer, and decision before replying.
Keep agent output summaries and evidence paths; do not copy raw tool transcripts.
The file is the record. Chat is not. Give each input an ID and draft/check work
an associated snapshot ID so stale results cannot overwrite newer decisions.

### Plan file

```markdown
# {short description}

Status: planning
Phase: initialize
Input: {input_id}
Snapshot: {snapshot_id}
Created: {datetime}

## Task

{user's task, verbatim}

## Log

### {datetime} — input {input_id}

{verbatim user message}

#### Similar implementations

{none, or one block per hit: name, path, what it does, why it is similar}

#### Question

{the question asked}

#### Answer

{pending, then the user's answer}
```

Add sections as they settle. Do not leave `TBD` or `TODO` in a settled section.

- **Decisions** — reuse, adapt, or skip, plus any design choice the user accepted.
- **Glossary** — one term, one meaning, written when `domain-modeling` settles it.
- **OKR** — cycle, owner, context summary (150 words or fewer), then the `okr-strategist` draft: at most 3 objectives, 2–5 key results each, baseline and target on metric results. A missing baseline stays `TBD` only until the user supplies it or explicitly skips it.
- **Language** — each language, the directories and files that will hold the code, and the skills from the table above. Filled and confirmed before **Design** is approved.
- **Design** — approaches considered, the chosen approach, architecture, data flow, errors, and how to tell it works. Scale length to the task. Draft sections as proposed during the interview, then record each explicit user approval. Mark Design confirmed only after every required section is approved. Key results are the measurable version of "how to tell it works"; do not invent a second, conflicting success check in **Design**.
- **Implementation plan** — the `writing-plans` document: goal, architecture, tech stack, global constraints, then bite-sized tasks. Each task names exact files, interfaces, a failing test, the minimal implementation, and the command with its expected output. No `TBD`, no "similar to task N", no step that says what to do without showing how. Each commit step is an atomic commit on the temporary branch. `implement-prepared-plan` merges those commits and does not squash them.


## State and resumption

Update Phase and input/snapshot IDs when advancing. Record confirmation state
for Language, OKR, and each Design section separately from draft content.
User assumptions or worker suggestions never count as confirmation.
On changed requirements, mark affected sections proposed again and invalidate
dependent implementation drafts/checks. Preserve the historical log. Resume
from the earliest affected phase; do not rerun unaffected lookups or approvals.
