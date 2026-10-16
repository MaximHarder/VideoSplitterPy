## Plan mode and language

Read `using-superpowers` first. Then enter or verify Plan mode before questions, exploration, or any other skill, following [Cursor runtime](cursor-runtime.md). Use the available SwitchMode capability with `target_mode_id` `plan` when a switch is needed. Say that the task will be planned into one plan file and that product code waits until the user leaves planning.

If the user rejects the switch, stop. Do not plan in Agent mode instead.

Stay in Plan mode until the user says the plan is finished or asks to leave Plan mode. Writes stay inside the plan folder: `plan.md`, `wayfinder.md`, and `design-mockup.md`.

While Plan mode is active, determine the programming language and the place the code will live. Do this before the design is approved. Use the memory search and the repo. Do not ask the user for a language or a path the codebase already shows.

- If a similar implementation is the basis, the language and the place are that code's language and its neighborhood, unless the user chooses otherwise.
- If the repo has one language in the area of the task, recommend that language and those directories.
- If more than one language or place fits, ask one interview question. Recommend one option and name the paths.
- Record the result under **Language** in `plan.md` and wait for the user to confirm it.

**Language** names each language, the directories and files that will hold the code, and the skills the implementer must use:

| Language | Skills |
| --- | --- |
| PHP | `php-pro`, `php-modernization` |
| JavaScript | `javascript-pro` |
| TypeScript | `typescript-pro`, and `react-expert` or `react-native-expert` when that is the stack |
| Java | `java-architect`, `spring-boot-engineer` |
| Python | `python-pro`, and `django-expert` or `fastapi-expert` when that is the stack |

A project rule that contradicts a generic skill wins. Name that rule in **Language**. The Tech Stack and every task path in **Implementation plan** must match **Language**. Do not leave either choice for the implementer to guess.

### DevCraft Admin plugin

If the place is a DevCraft Admin satellite, or the user says the work is one, read both skills before the design is approved:

- `/home/maxim/Dev/PHP/dle210.test/.cursor/skills/create-devcraft-plugin/SKILL.md`
- `/home/maxim/Dev/PHP/dle210.test/.cursor/skills/check-devcraft-plugin/SKILL.md`

Signs: `devcraft/src/modules/`, or `install.xml` with `needplugin=DevCraft Admin`.

Record the mode (`создание`, `перенос`, or `обновление`), `{Name}`, `{code}`, `{mod}`, `{version}`, and the profile from the check skill. For a missing fact, follow [the shared interview rule](interview.md): one question per message without a similar implementation, or one grilling frontier round when a match exists. The plan's checks are that profile's checklist. Do not invent a canon item. Do not raise the package version unless the user asks.

