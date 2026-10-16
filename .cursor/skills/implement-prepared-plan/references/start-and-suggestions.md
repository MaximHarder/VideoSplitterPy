# Start and workspace authorization

Before product code, make the prepared results reviewable: checklist, tasks,
context, resolved analysis, and the alternative refactor proposal. Do not create
or switch branches yet. Carry forward explicit authorization/preferences already
given in this session; do not re-ask a question already answered.

If start approval is missing, ask one question: start implementation, or add a
suggestion? Wait for an explicit answer. Unrelated replies are not authorization.
If temporary-branch preference is missing after start approval, ask:

> Do you want an isolated temporary branch starting from the current state,
> including uncommitted changes, then merged without squash back into the
> recorded branch? Owned temporary resources are removed only after safe integration.

A combined start/branch answer counts. Branch consent authorizes worktree setup,
atomic task commits on that branch, and non-squash integration; do not request
that same consent again. A declined temporary branch means work stays on the
recorded branch: no branch switch, merge, or cleanup. Commits there require the
user's explicit commit authorization; otherwise leave edits uncommitted.

If still in Cursor Plan mode after both gates pass, use the actual mode-switch
capability to enter an editing-capable mode, or ask the user to select it when
unavailable. Do not use nonexistent tools or bypass permission restrictions.

For suggestions, use `grill-with-docs`, `grilling`, and `domain-modeling`: ask
only unresolved choices, offer options, and wait. Use repository evidence for
facts. Apply an unambiguous authorized suggestion to tasks/checklist/context;
append an Adjustment only if the source changes. Recheck affected analysis and
approval state. A material change outside the approved scope requires renewed
approval for that change; ordinary task repair does not restart both gates.
Do not implement the alternative refactor plan unless explicitly adopted.

Append each suggestion to `suggestions.md` in this interview shape. One section per suggestion. Do not create the file before the first suggestion.

```markdown
# Extra suggestions and informations

Date: {datetime}
Context: `{version_id}-{short-description}`
Last update: {datetime}

## {suggestion}
{for all questions}
### {question}

#### Reply options

- {option}

#### Users intend / answer / option selected

{what the user decided}
{endfor}
```

When the suggestion has no open question, still write the section: put the suggestion under `##`, and under `### User intend / answer` write what the user asked to change. Leave `#### Question asked` and `#### Options provided` as `—`.

After the answer, apply it to `tasks.md`, and to `checklist.md`, `context.md`, or `plan.md` when the suggestion changes those. Ask whether to start again only when start consent is still missing or a material scope change needs approval that the suggestion did not already give. Preserve existing authorization for ordinary clarifications. A suggestion alone does not grant start approval. If the same message explicitly authorizes the revised implementation and provides the branch choice, honor that authorization after affected preparation checks pass.

