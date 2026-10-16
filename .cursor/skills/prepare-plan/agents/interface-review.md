# Read-only interface-option briefing

Use this as the prompt for one interface alternative after the completion gate.
Supply the validated snapshot ID, task, approved Language/Design/OKR, the selected interface alternative,
relevant repository evidence, and the vocabulary from `codebase-design` and its
`DESIGN-IT-TWICE.md`. Give each alternative its own Task call when available.

Describe this option as a module mockup: module responsibility, public interface,
seam, depth, adapter, data flow, failure behavior, and trade-offs. Keep paths and
languages consistent with the approved plan. Show interface sketches only as
planning text, not as executable product files. State uncertainties explicitly.

Do not write files, implement, scaffold, commit, or override user decisions.
Return snapshot ID, a concise proposal with path:line evidence, trade-offs,
and uncertainties. Follow [the result contract](../references/context-management.md).
No recursive delegation or silent changes to approved decisions. The parent compares alternatives and
writes `design-mockup.md` inside the active plan folder.
