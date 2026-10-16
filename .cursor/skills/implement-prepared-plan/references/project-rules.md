# Applicable implementation skills and project rules

Load only guidance matching the actual task and repository, before its first edit.
Project instructions override generic skills. Resolve Language and paths from the
approved plan; stop and clarify a material mismatch instead of changing stacks.

When a task writes or changes SQL, follow `sql-optimization` while writing it and `sql-code-review` on the result. When a task creates or edits a GitHub Action or a file under `.github/workflows/`, follow `github-actions`. If that skill is not installed, stop and say so. Do not invent the workflow.

When a task writes documentation or a user-facing description, write it at ELI18: short sentences, plain words, a gloss for any term that is not everyday speech. Use `documentation-writer` for the document type, `copywriting` for product description, `ai-seo` when the text should be citable by AI search, and `programmatic-seo` when many pages share one template. Skip a skill that does not match the task.

## Language skills

See which language the plan's code is in. Use the matching skills while writing that code. Combine them when the change spans languages.

| Language | Skills |
| --- | --- |
| PHP | `php-pro`, `php-modernization` |
| JavaScript | `javascript-pro` |
| TypeScript | `typescript-pro`, and `react-expert` or `react-native-expert` when that stack is the one in the plan |
| Java | `java-architect`, `spring-boot-engineer` |
| Python | `python-pro`, and `django-expert` or `fastapi-expert` when that stack is the one in the plan |

Project rules that contradict a generic skill win. Example: DevCraft PHP uses tabs and Russian comments, and Cycle entities stay writable.

## DLE and DevCraft

If the plan is for DLE or a DevCraft Admin satellite, read and follow:

- `dle210.test/.cursor/rules/devcraft-reuse-first.mdc`
- `dle210.test/.cursor/rules/devcraft-public-assets.mdc`
- `dle210.test/.cursor/rules/russian-eli18.mdc`

If the change touches Twig or Metro markup, use the Metro docs as the reference for components, scripts, styles, and libraries:

- `metroui-docs/src/content/docs/components`
- `metroui-docs/src/content/docs/common-js`
- `metroui-docs/src/content/docs/common-css`
- `metroui-docs/src/content/docs/libraries`

## Repository-specific lookup rules

For unknown code locations, follow Graphify-first discovery in [Cursor runtime](cursor-runtime.md), then the applicable memory sources below. Resolve repository-specific rule paths against the actual project; do not load DLE rules in unrelated repositories or invent unavailable files.

- skill `codebase-memory`
- `dle210.test/.cursor/rules/caveman.mdc`
- `dle210.test/.cursor/rules/cavemem.mdc`
- `dle210.test/.cursor/rules/code-review-graph.mdc`
- `dle210.test/.cursor/rules/codebase-memory.mdc`
- `dle210.test/.cursor/rules/graphify.mdc`
- `dle210.test/.cursor/rules/mem0.mdc`

## Large flows

When the information is large or the steps branch, follow `dle210.test/.cursor/rules/sequential-thinking.mdc` before coding further.

