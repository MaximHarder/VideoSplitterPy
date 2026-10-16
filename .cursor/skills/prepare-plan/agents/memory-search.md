# Read-only memory-search briefing

Parent supplies stage (`orientation` or `connected-memory`), input ID, latest
user text with original task/current question/accepted decisions, previous hits,
absolute project/plan paths, available tools, and prior orientation
when applicable. Read [evidence order](../references/memory-search.md) and obey
[the result contract](../references/context-management.md).

Do only the assigned stage. For orientation, prefer exposed Graphify MCP tools
(`query_graph`, then relevant `get_node` / `get_neighbors`) and supply the absolute
`project_path` when supported. Do not gate MCP on local graph files. Verify graph
identity and follow the documented local CLI/wiki fallback if MCP is unavailable.
Return matching paths, neighborhoods, graph/project identity, and limitations.
For connected-memory, use the parent-provided orientation and search available
memory sources in the documented order. Do not repeat graph work or broad raw
repository scouting assigned to another worker.

Return status, input ID, concise hits (qualified name, path:line, behavior,
match reason), unavailable sources, and uncertainties. No invented matches,
file writes, product code, commits, user questions, or recursive delegation.
The parent records the findings.
