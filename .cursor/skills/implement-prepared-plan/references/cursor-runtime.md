# Cursor tools, Graphify MCP, and optional Grok

## Skill and tool discovery

Cursor loads SKILL.md from `~/.cursor/skills/implement-prepared-plan/` when explicitly
invoked; preserve `disable-model-invocation: true`. Resolve links against this folder.
`agents/` holds loaded prompt templates, not automatically registered custom agents;
openai.yaml is optional UI metadata for other hosts. No separate registration is needed.

Find skills in the session catalog, project/user `.cursor/skills/`, shared
`~/.agents/skills/`, built-in `~/.cursor/skills-cursor/`, and installed plugins.
Do not hard-code plugin cache versions. Use exposed Cursor Task/workspace/mode
capabilities, not fictional shell commands. Task unavailable means sequential
main-agent work with the same approval/write boundaries and explicit limits.
Check editing mode only after the start/workspace gate; no product edits in Plan mode.

## Graph-first discovery for unknown facts

Prefer connected Graphify MCP. Discover actual tool schemas; configuration alone
is not a live connection. Do not require a local graph file before trying MCP.
Use the absolute `project_path` when supported, and verify returned evidence belongs
to the agreed repository/workspace. A server-default graph for another project is
not evidence. Worktree graphs may describe the baseline checkout; verify mutable
symbols and changed code against the actual implementation workspace.

Use read-only `query_graph`, then needed `get_node` / `get_neighbors`; use
`shortest_path` for relationship questions and `graph_stats` for availability if
exposed. Use bounded token_budget (about 1000–2000) when supported. Do not invent
MCP query/explain names. One investigator supplies shared graph orientation;
only then may independent raw source scouts start. Retain valid orientation,
but refresh facts after code edits that make indexed relationships stale.

If MCP cannot serve this project, report unavailable/error/no-graph distinctly.
Fall back to local Graphify CLI query/explain with the correct project graph,
and read an existing graphify-out/wiki/index.md before raw graph artifacts.
Then use scoped read-only source search if graph orientation is unavailable.
No graph rebuild, installation, restart, or MCP config change just for discovery.

Connected memory sources can supplement orientation: codebase memory
list_projects/search_graph/search_code, code-review graph, cavemem search,
Mem0 search_memories, and caveman notes for past sessions. Match actual names
by function, skip unavailable sources, and distinguish no hits from no connection.
Do not repeat known lookups or fetch full files into the main chat unnecessarily.

## Optional Grok second opinion

A local `/usr/bin/grok-bot` desktop launcher exists, but no callable Grok CLI/MCP
interface was established during the related prepare-plan update. A launcher
alone is not a prompt/response API or evidence of local model inference.
Use Grok only through a documented interface exposed in the session or supplied
by the user, when useful for bounded read-only review of a stable diff, acceptance
criteria, or a difficult alternative. Return findings with evidence and uncertainties.
Verify its claims and do not let it change authorization, shared Git, or product files.
If unavailable, continue normally; manual returned feedback can be clarified.
Do not invent flags/endpoints, launch the desktop UI, or automate it as an API.
