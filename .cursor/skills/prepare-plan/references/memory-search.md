# Evidence loop for every input

Log the original task or latest user input before lookup. Supply its input ID,
project root, absolute plan path, original task, current question, accepted
decisions, previous hits, and available tool names. Resolve short answers such
as "option 2" against that question rather than searching their literal text.
For an acknowledgment without new scope, the agent may return still-valid
evidence without repeating broad searches. Before the next
interview question, delegate the following stages using
[the memory briefing](../agents/memory-search.md).

## 1. Shared graph orientation

Prefer the connected Graphify MCP server. Discover its actual tool schemas in
the current Cursor session; configuration alone does not prove it is callable.
Do not require a local `graphify-out/graph.json` before attempting MCP orientation.
Select the current project explicitly with the absolute `project_path` when the
exposed schema supports it, and verify that returned paths belong to that project.
Do not use an unrelated server-default graph as evidence for this task.

Use read-only `query_graph` for the request, then `get_node` / `get_neighbors`
for relevant hits. Use `shortest_path` only when a relationship needs tracing;
`graph_stats` can help diagnose graph availability. These are tool names in the
installed Graphify version; adapt to the exposed schemas rather than inventing
MCP `query` or `explain` calls. Set a bounded `token_budget` when supported
(about 1000–2000 tokens per query) and narrow further queries using the first hits.
Do not fetch entire communities unless needed for a concrete open question.

If MCP is unavailable, fails, or has no graph for this project, log that distinct
state. Fall back to local Graphify CLI query/explain when available with the
correct project graph. Read `graphify-out/wiki/index.md` before other local graph
artifacts when present. If neither MCP nor local Graphify can orient the task,
record the limitation and allow scoped read-only repository search. Do not
build/reindex graphs, restart servers, or change MCP configuration while planning.
A missing graph file in the local workspace is not proof that the MCP server
has no graph; an empty query is not proof the server is unavailable.

Return matching symbols, paths, relevant neighborhoods, graph/project identity,
and gaps. This stage's result (including a documented fallback) is the barrier
before raw repository scouting; do not independently repeat orientation in every
worker. Reuse still-valid orientation for later inputs and have the lookup agent
check whether the new scope requires a refresh.

## 2. Independent lookups after orientation

Run connected-memory lookup and [repository scouting](../agents/repository-scout.md)
in parallel when repository facts are unknown. Memory sources are searched in
this order; skip disconnected servers and match actual tool names by function:

1. Codebase memory: `list_projects`, then `search_graph` and `search_code`.
2. Code review graph when connected.
3. Caveman memory: `search` on cavemem.
4. Mem0: `search_memories`.
5. Caveman notes: `caveman_retrieve` for past-session notes.

Graphify hits and source search remain evidence even without memory servers.
Repository scouts may read/search files after shared graph orientation or
after MCP/local orientation limitations are recorded. Scope scouts to
facts not already established: language, code location, project rules, reuse
candidates, interfaces, or verification commands. Do not duplicate known facts
or ask the user for facts the repository can supply.

## 3. Join and record

Workers return hits: qualified name, file path (line when available), behavior,
and why it matches. Distinguish no hits from unsearched/unavailable sources;
never invent a match. Follow the compact result contract in
[delegation](context-management.md). The main agent merges/deduplicates results
under the current input's Similar implementations, logs limitations, and then
chooses the appropriate interview path. No source match is a valid result;
unavailable servers alone do not establish that no implementation exists.
