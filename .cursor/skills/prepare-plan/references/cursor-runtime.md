# Cursor runtime and optional Grok Bot

## Cursor skill loading

Cursor discovers this skill through `SKILL.md` in `~/.cursor/skills/prepare-plan/`.
Keep `name`, `description`, and `disable-model-invocation: true` in its YAML
frontmatter. Invoke it explicitly with `/prepare-plan` or the skill mention.
Resolve references and agent templates against this skill directory, regardless
of the current project. `agents/openai.yaml` is not Cursor subagent registration
and is not required for this workflow.

Find named skills in Cursor's available-skills catalog first. If needed, search
project `.cursor/skills/`, user `~/.cursor/skills/`, shared `~/.agents/skills/`,
Cursor's built-in `~/.cursor/skills-cursor/`, and installed plugin skills.
`create-subagent` is currently in `~/.cursor/skills-cursor/create-subagent/SKILL.md`.
Superpowers skills can come from an installed plugin; discover their current
path instead of hard-coding a plugin cache version. Read each skill before use.
If a required skill is unavailable, report which one and pause its dependent
phase; do not claim to have followed it. Other independent preparation may proceed.

## Modes and tools

Use the tools actually exposed by the current Cursor session. `SwitchMode`
and `Task` in the references name Cursor capabilities, not shell commands.
If already in Plan mode, do not require another switch. Otherwise use the exposed
mode-switch tool. If unavailable, ask the user to select Plan mode in Cursor
and wait before exploration or planning; never silently continue in Agent mode.

Follow [the delegation contract](context-management.md) for Task jobs, phase
barriers, compact results, and single-writer ownership. Read the relevant prompt
template from the skill's `agents/` directory and supply a bounded brief.
These templates are not automatically installed custom subagents; do not copy
them to `.cursor/agents/` or `~/.cursor/agents/` unless requested.
If Task is unavailable, perform the same jobs sequentially in the main planning
context and log that fallback; approval gates and write boundaries still apply.

MCP names vary by session. Match connected servers by function rather than
requiring the literal `user-` namespace from the references. Missing memory
servers do not mean there are no matches. Record unavailable sources separately
from sources searched without hits. Do not install servers or change configuration.
Graphify MCP is the preferred graph interface. Discover the connected tools and
supported parameters; use the current project's absolute `project_path` when
supported. A configured server is not necessarily connected in this session.
Do not require local graph files for MCP use. Follow [the evidence loop](memory-search.md)
for read-only tools, project identity, output limits, and CLI/wiki fallback.

If Plan mode cannot write the planning artifacts, explain the limitation and
wait for a supported way to save them. Do not change modes or claim persistence
that did not happen. Product code stays untouched.

## Optional local Grok Bot

A Grok Bot desktop launcher was found at `/usr/bin/grok-bot`, resolving to
`/opt/Grok Bot/grok-bot`. Its desktop entry launches `grok-bot %U`.
No callable Grok CLI or Grok MCP server was found during this update.
The launcher alone is not a documented prompt/response API, and installation
on this machine does not establish local model inference.

Use Grok only when an actual documented interface is available and its output
can be read back. Suitable jobs are a second opinion on competing interfaces,
missing acceptance criteria, or inconsistencies in the prepared plan. Avoid an
extra call for routine logging or every interview message.

Discover the interface from the session's connected tools or user-provided
documentation. Do not invent flags, endpoints, model names, or URI payloads.
Give it a bounded read-only brief: the task, relevant plan excerpt, alternatives,
constraints, and the specific question. Require findings with evidence,
uncertainties, and suggested changes; no product writes, commits, or execution.
Validate its claims against the repository and append useful findings and the
accepted or rejected decisions to `plan.md`. User confirmations remain required.

If no callable interface is available, continue with Cursor's normal workflow
and record that Grok was unavailable when relevant. A user may obtain a manual
second opinion in the desktop app and return it to the interview. Do not launch
the app automatically or automate its UI as though it were an API.
