# Interview and decision gates

Before interviewing, read the interview skills in
[skill routing](skill-orchestration.md). For every new user input, log it and
complete [the evidence loop](memory-search.md) before the next question.
The main agent asks questions and records answers; workers only supply facts
or proposals. Do not ask for facts already available from the repository.

## 1. Scope and reuse

When a similar implementation was found, base the next step on it. Ask one
numbered grilling frontier round about reuse, adaptation, or skipping it.
Recommend an option with its evidence path and wait. Do not design a separate
new approach until the user sets the existing one aside. Later questions concern
how to use/adapt the chosen code.

If no match was found, state the search result and any unavailable sources.
Use brainstorming: one question per message, multiple choice where useful,
with a recommendation. Establish purpose, constraints, and success criteria.
Never infer that disconnected servers prove no implementation exists.

Questions dependent on an open answer wait for the next round. Write settled
terms to Glossary and accepted choices to Decisions immediately.

## 2. Approach, language, and placement

When scope is clear, compare 2–3 approaches with trade-offs and a recommendation.
If found code remains the basis, the alternatives are reuse, adapt, and skip.
Delegate independent bounded alternative analysis when useful; the main agent
synthesizes and asks for the choice. Do not load `codebase-design` for the final
mockup yet or launch its post-completion work prematurely.

Follow [language and DevCraft rules](plan-mode-and-language.md). Derive Language
and paths from evidence where possible and obtain explicit confirmation. Resolve
any applicable DevCraft profile before presenting the design for approval.

## 3. Measurable outcomes

Once approach and Language are settled, read `okr-strategist`. Draft OKR in the
existing plan, run its global validation checklist, present it, and wait for
confirmation. Objectives stay qualitative; key results are measurable with
baseline and target. Prefer metrics, then milestones. Mark skipped questions
and missing baselines as explicit assumptions rather than inventing values.
An explicit waiver may resolve missing data; assumptions are not approvals.
Use the same one-question/frontier rules instead of a five-question batch.
For an existing OKR follow that skill's review SOP; for actual results use its
retrospective SOP in the same section.

## 4. Design approval

Draft Design sections as `proposed`, aligned to confirmed OKR success criteria.
Present each section and wait for approval; record its state in the plan.
Cover architecture, components, interfaces, data flow, errors, and verification
only as far as needed. Offer the brainstorming visual companion only when the
question is clearer visually. Text questions stay in chat.

Do not approve a section on the user's behalf. Language, OKR, and all Design
sections must be confirmed, with no open dependent decisions, before drafting
implementation tasks. If a design change affects a confirmed outcome or language,
reopen that decision, align the sections, and obtain confirmation again.

## 5. Implementation drafting

Read `writing-plans` after the approval gate. Freeze the approved interfaces,
paths, success criteria, and Global Constraints. Delegate independent task
groups under [the drafting briefing](../agents/plan-draft.md) when useful;
otherwise draft directly. Integrate them into Implementation plan in `plan.md`,
resolve task numbering and dependencies, then run self-review and the parallel
checks in [completion](completion-and-mockup.md). Do not execute the plan.
