# Workspace, atomic commits, and integration

## Baseline before preparation writes

The parent records `git branch --show-current`, `git rev-parse HEAD`, repository
and checkout paths, tracked staged/unstaged paths, and untracked paths. Before any artifact write, preserve the actual pre-existing file/index content,
including existing plan records, using a recoverable non-destructive snapshot/copy
mechanism. Only then record start in review-range.md and dirty attribution in
context.md. A recoverable baseline must exist before preparation or transfer; status names or hashes alone cannot recover it.
Record where that baseline lives without exposing secrets in chat. Distinguish
user-owned edits from implementation edits even when they share a file.

Do not stash, reset --hard, clean, checkout --, or restore files to empty the
tree. Do not commit unrelated user work. A dirty tree is not a refusal reason;
stop only when the requested transfer/integration cannot preserve it, or Git
would overwrite it. Never discard staged, unstaged, or untracked content.

## After start and branch gates

Load `git-workflow-and-versioning` for atomic work. Respect an available mandated
Git provider (for example `but`) for mutations; CLI command names here describe
operations, not permission to bypass that provider. Parent performs all Git
mutations serially; agents never stage, commit, switch, merge, or stash.

For a temporary branch, load and announce `using-git-worktrees`. Detect existing
isolation; use native workspace tools first and a supported Git worktree fallback
only when native tools are unavailable. Record which resources are owned by this
run. Do not delete a pre-existing/harness-owned worktree or branch.
Name an owned branch `fix/<short-description>` for bugfixes, otherwise
`feature/<short-description>`; use the source folder slug without its NNN prefix.
Start from the recorded commit and preserve the current dirty state, not a fresh
unrelated trunk. Do not silently fall back to working in place after isolation
fails; retain the agreed workspace choice and report the blocker.

Transfer baseline tracked/untracked content, including index state when relevant,
non-destructively to the isolated workspace with a mechanism proven to preserve
it. Verify against the baseline before editing. Keep original paths intact.
If a path cannot be transferred safely, stop and report it. Do not run setup or
installation merely because a manifest exists; use the plan's required commands.
Do not auto-commit unrelated .gitignore/setup changes to create isolation.

If temporary branch was declined, remain on the recorded branch. Skip creation,
branch switching, merge, and temporary cleanup. Atomic commits on this branch
need separate explicit consent; otherwise keep task and record edits uncommitted.

## Commit validated slices

After independent task checks pass, inspect changes against the baseline and
stage only the task's attributable hunks/paths. Commit authorized slices serially;
include plan records where appropriate. Do not capture another worker's changes
or pre-existing staged user edits. If selective staging cannot separate them,
resolve attribution before committing. Preserve user-owned edits uncommitted
and their staged/unstaged intent. Never squash or cherry-pick from another base.

## Review and non-squash merge

Refresh end to the implementation HEAD after every repair/commit. Review start
to end plus staged, unstaged, and untracked implementation changes with baseline
attribution; SHA endpoints alone do not include uncommitted work.
Only integrate after the final checklist/review gate passes. Stop workers first.
Check the recorded checkout for changes since the baseline. A merge must retain
both original user work and validated implementation results, including plan
records. Use a regular non-squash merge; a fast-forward is acceptable.

Do not copy an isolated dirty tree blindly over the recorded checkout. Reconcile
only attributable implementation edits using the baseline, and preserve original
user-owned content and index state. If changes conflict, overlap cannot be safely
reconciled, or Git would overwrite existing files, stop without stashing/discarding;
leave the implementation branch/worktree intact and report both branches and paths.
Do not fabricate a merge result or force cleanup.

After successful integration, verify target content and appropriate checks.
Remove only owned temporary resources when all wanted content, including every
remaining dirty change and its staged/unstaged intent, is proven preserved in the
target. Duplicated baseline dirt alone does not mean integration failed. Use no
forced worktree removal or forced branch deletion; if the available tool cannot
safely remove a dirty workspace without force, leave it intact and report that
cleanup limitation. Unique, untransferred, or unresolved content always blocks cleanup.
Report the recorded branch, integration HEAD (or merge commit when one exists),
checks, retained dirty state, and any remaining resources. Never push or open a PR;
`finishing-a-development-branch` does not apply.
