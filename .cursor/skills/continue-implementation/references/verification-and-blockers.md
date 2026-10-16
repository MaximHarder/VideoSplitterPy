# Manual checks and other interruptions

## Manual-test handoff

A label such as "manual test" is not itself a reason to stop all work. Read the
acceptance item and determine what observation it actually requires.

1. If the session has a suitable browser, debugger, local application tool, or
   command, perform the check within the authorized environment/scope. Use real
   observable outcomes, not assertions that merely mirror implementation code.
2. If a focused existing automated check proves the same acceptance condition,
   use it and record what it covers and any limits. Do not replace visual or
   interaction acceptance with a build/lint pass that proves something else.
3. If the check requires unavailable hardware/access, a user judgment, an external
   credential/action, or an unavailable tool, keep it pending. Record the procedure,
   environment, expected result, and exact missing input. Do not silently waive it,
   invent a result, install a new testing stack, or broadly rewrite the app to test it.

Continue all dependency-ready authorized tasks and other checks while the pending
item waits. A task/check dependent on that observation remains blocked. Separate
"implementation complete" from "acceptance verified" in tasks/checklist rather
than marking a partially verified task done. Required pending acceptance still
blocks the original final integration gate unless explicitly resolved by the user.
A returned user result can resolve a check when it addresses the actual criterion
and relevant version/environment; distinguish user-reported from agent-observed
verification. Changed code/environment can invalidate old results.
An explicit user scope/acceptance change is recorded as an accepted Adjustment;
a request to continue alone is not that change.

## Other stop reasons

| Interruption | Resume action |
| --- | --- |
| Failing check or reviewer finding | Inspect evidence; fix only the authorized gap; rerun relevant checks. Existing baseline failures are identified separately. |
| Session/context ended | Recover records and live jobs; resume the first unfinished dependency-ready slice, preserving valid work. |
| Tool/service/connection unavailable | Check current availability; use an equivalent supported fallback with honest limits; continue unaffected work. |
| Existing manual checklist ignored automation | Attempt the relevant observable check with available tools before handing it back again. |
| Approval or unresolved scope | Retain earlier approvals; ask only for the missing material decision and continue independent preparation. |
| Merge would overwrite user work | Retain both states; follow the original Git preservation rules; no stash/reset/force cleanup workaround. |

For tool failures, make a diagnostic attempt and use available evidence to choose
an appropriate alternative. Repeat only after a relevant input/environment change
or with a materially different justified approach; do not retry the same blocked
action in a loop. Respect permission denials and external action boundaries.
Known non-idempotent operations require checking prior outcome before any retry.
A local test may modify approved test fixtures; it does not imply permission to
write production data, deploy, message others, or obtain missing credentials.

If every remaining action depends on unavailable input/tool/access, end with the
exact checkpoint and required next action. Report implementation/verification
states separately. Do not claim completion, wait indefinitely, or demand that the
user repeat a check they already reported with sufficient evidence.
