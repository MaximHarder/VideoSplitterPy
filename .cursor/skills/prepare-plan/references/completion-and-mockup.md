# Validation, mockup, and final review

## 1. Validate the integrated implementation plan

Prerequisite: Language, OKR, and Design are explicitly confirmed and the
implementation draft is complete. Assign one snapshot ID to that frozen draft.
The main agent runs `writing-plans` self-review: specification coverage,
placeholders, and type consistency. When useful, delegate coverage and feasibility
checks in parallel using [the check briefing](../agents/plan-check.md).
Workers read the same snapshot and do not edit it. Join their results, resolve
findings inline, and repeat only checks invalidated by material changes.

The completion gate passes only when the interview frontier is empty, Language
is confirmed, all Design sections are approved, OKR is confirmed, the plan has
passed self-review, material worker findings are resolved, and approved sections
and task instructions contain no unresolved placeholder. Commands, expected
outputs, interfaces, paths, Tech Stack, and future atomic commit order must agree
with the approved decisions. Log remaining verification limits explicitly.
Do not call the plan ready because workers returned or the draft exists.

## 2. Module mockup after the gate

Read `codebase-design` and `DESIGN-IT-TWICE.md` beside that skill. Prepare concrete
interface alternatives from the approved plan. Use
[the interface briefing](../agents/interface-review.md) for each independent
alternative; run them in parallel when Task is available and the work is useful.
Use the fallback in [Cursor runtime](cursor-runtime.md) otherwise. A documented
Grok interface may provide an optional independent second opinion; its absence
does not block planning.

Use the vocabulary module, interface, seam, depth, and adapter. Compare proposals
and write `design-mockup.md` inside the active plan folder; no product code.
The mockup must describe the approved Design. If an alternative changes an
approved interface, language, scope, or outcome, present the proposed change,
mark affected sections proposed, obtain renewed user confirmation, then revise
dependent tasks and rerun affected checks before finalizing the mockup. A late worker proposal cannot silently replace
the approved plan.

## 3. Final user review

Ask the user to read `plan.md` and `design-mockup.md` and identify final changes.
Route new inputs through the evidence/decision loop and rerun affected phases.
Only after the user finishes planning may Status become ready. Do not implement,
offer automatic execution, or switch to Agent mode without the user's request.
Implementation remains a separate request.
