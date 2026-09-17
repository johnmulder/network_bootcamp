# Learner Pilot Worksheet

Status: ready to use; no learner pilot results have been recorded here.
A technical walkthrough is not a substitute for observing learners.

Copy this worksheet under `work/` for each pilot. Use anonymous participant
labels. Record beginner/experienced background and solo/pair mode; avoid
collecting names or other unnecessary personal data.

For guided delivery, export progress with `./course session export --id LABEL
--format csv` (put the command on one line). Use `--format json` for ratings,
versions, and separate self/facilitator review status. Default exports omit
answers and review comments. Explicit `--include-artifacts` with JSON or
Markdown includes the four learner files and response/review history for review.
The [delivery guide](../delivery/README.md) explains local exports and revisions.
Timestamps and self-reported durations do not measure active learning; observe
and record active minutes here. Scripted rehearsal scores are not learner data.

Date / facilitator / participant count / modes: ___

## Pilot Sequence and Comparison Design

Human validation is pending. Arrange participants and facilitator time before
claiming a trial: first observe one beginner and one experienced learner in the
transfer slice, then repair blocking friction and run one complete beginner
solo day and one paired day with separate individual exits. Do not replace
participants with scripted answers. Keep each course version with its records;
use new sessions after changing assessed content.

For the slice, observe prediction, incorrect or correct first response, support
choice, and a fresh reassessment. A successful first responder can bypass help.
For the full day, compare the initial route-selection task with a reserved
equivalent fresh variant near the end. Reserve the first `route-selection`
reassessment for three minutes within the ten-minute capstone review, leaving
seven minutes for that review; do not add time or consume the A/B exit packet.
Revisit `c01.change` and choose `reassess`, then return to the current phase.
If both variants were already exposed, record the comparison as unavailable;
do not call a retry unseen. Additional second attempts belong after class.

Use the same objective and rubric when comparing responses, and record the
different variant's conditions. Report individual learners as the denominator,
not attempts or pair submissions. Compare first attempts, supported corrections,
and unassisted fresh results separately. A small observed sample supports a
revision decision, not a general claim that the teaching technique works.

Course version / content hash / fixture hash: ___

Pilot stage / anonymous learner labels / prior background / support exposure:
___

Initial objective and variant / later equivalent variant / interval between:
___

## Curriculum 3.1 Trials

Keep optional LLM support disabled for these curriculum trials. Record the
course version and diagram condition before the learner sees an answer.
The optional model comparison below is a separate later study.

### Beginner Foundations Slice

Use the opening local/remote diagnostic, then Challenge 1's existing ten-minute
model: six minutes of worked `/24` and IP/MAC reasoning, four of prediction.
The illustration replaces vocabulary-tour time. Observe a fresh `subnet`
reassessment in `opening.predict` after support, using the taught first-three-
octets method. Ask for both the packet IP destination and next-hop MAC in an
explanation; the yes/no check alone does not assess both headers. Keep `/25`
and `/23` optional and separate. Record whether a prerequisite or boundary
operation was unfamiliar. Stop and repair blocking instructions before a day.

Compare the illustrated explanation with baseline commit `a138967` using
separate, similarly experienced beginners. Preserve both course copies and
never open one version's saved session in another. Keep task difficulty at
`/24`, the same time allowance, and the same human rubric. Do not expose a
learner to both answers and call the second result independent. Record group
assignment, prior experience, help, navigation time, and diagram-reading errors.
A tiny convenience sample supports editorial decisions, not a causal estimate.

### Evidence Choice and Exit Timing

During Challenge 5 Round 3, let the learner choose `incident.round3` (the
firewall/NAT/proxy bundle) or `flows` (intended flow matrix) first. Both are
released in
that phase; earlier rounds have only one view. Record the predicted value,
show the selected view, then show the other before advancing. Use `evidence`
actions or the manual commands; do not preview a later phase or reserved case.
Compare the initial claim with the revised claim and ask which observation
changed the next action. Record all help exposure as usual.

First observe the published five-minute `exit.answer`. If command navigation
and writing crowd out reasoning, trial ten minutes by taking five from the
capstone exchange: handoff becomes 50 minutes and exit 20, still 70 combined.
Keep the peer handoff, separate individual answers, review, and feedback.
Facilitate this as a documented timing trial; do not silently edit session
budgets or claim the published schedule was achieved. Change the authoritative
agenda and phase budgets together only after reviewing observations.

| Learner / phase | Instruction min | Navigation min | Evidence analysis min | Writing min | Active min | Difficulty or unavailable evidence |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

Use non-overlapping timer categories for elapsed teaching time. Active minutes
are a separate observation and may include analysis, explanation, and writing;
do not double-count simultaneous partner activity. Record marker/CSV repair,
exit navigation, and whether the learner understood hint consequences.

### Delayed Follow-Up

Reserve an unseen equivalent variant for an optional follow-up 3–7 days later.
Choose the family before the first session and log which finite variant remains.
Keep a route variant for the same-day comparison above; the remaining subnet
variant is a candidate if unexposed. If all variants have been seen, mark a
fresh follow-up unavailable instead of reusing an answer as retention evidence.
Record the interval, independent first result, outside practice, help exposure,
and missing follow-ups with individual denominators. Do not infer retention
from the same-day comparison.

### Second Human Review

A second reviewer checks the corrected IPv4/IPv6, STP, FHRP, and evidence-limit
claims against their nearby sources and saved observations. Independently score
one packet, architecture, and incident explanation using the objective anchors
in the [assessment contract](../delivery/assessment.md). Record disagreements
and the cited passage, reconcile the rubric interpretation, and keep raw
learner work private. Automated answer agreement does not complete this gate.

## Technique Observations

| Learner / phase / objective | Trigger or error code | Support level and whether requested | Feedback resolved the misconception? | Fresh variant / help exposure / first outcome | Evidence for observer judgment |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

| Learner / case | Initial diagnosis before any cue? | Confidence before evidence | Requested next evidence | Actual first view / next choice | Confidence after evidence | Claim changed and why |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

Record accidental cues from wording, filenames, a partner, or prior browsing.
Answer-bearing help changes assessment eligibility; orientation does not.
Distinguish incorrect reasoning from an invalid input format or command failure.
Record whether the learner could state why an experiment's result changed and
which uncertainty remained. Note repeated typing, marker repair, or review
navigation that consumed investigation time.

| Learner / reviewed artifact region | Self scores by dimension | Facilitator scores by dimension | Disagreement and cited passage | Revision / later scores |
| --- | --- | --- | --- | --- |
| | | | | |

## Local Data Collection

Use separate anonymous sessions, including for partners. Save raw worksheets
and exports under ignored `work/`; do not commit private free-text work.
Default JSON exports include per-objective attempt counts, first-response outcomes,
supported corrections, fresh attainment, variant IDs, support use, error codes,
review revisions, evidence-view order, and optional confidence/engagement data.

```sh
./course session export --id pilot-01 --format json --output observations.json
./course session export --id pilot-01 --format objectives-csv --output objectives.csv
./course session export --id pilot-01 --format csv --output phases.csv
```

These commands create new files inside that session's `exports/` directory and
refuse overwrites. Use `--include-artifacts` only when you intend to include the
learner's answers and prose for human review. Do not merge those raw exports
into a public aggregate. Confidence is optional and distinct from correctness;
`answer` and `submit_artifact` accept `confidence: low/medium/high`.

Process timestamps indicate recorded actions. Durations submitted on `continue`
are self-reports. Only the observer's worksheet measures observed active minutes.
Label missing observations as missing; never infer active time from elapsed
process time. Commit only an appropriate aggregate with participant counts,
raw outcome totals, unresolved issues, and the next validation decision.

## Observations

| Block | Planned minutes | Actual minutes | Active student minutes | Hints / friction / misconception |
| --- | ---: | --- | --- | --- |
| Opening | 15 | | | |
| Packet | 65 | | | |
| Transfer | 45 | | | |
| Link | 40 | | | |
| Resilience | 60 | | | |
| Incident | 65 | | | |
| Handoff | 55 | | | |
| Exit | 15 | | | |
| **Total** | **360** | | | |

Installation/support time outside instruction: ___

Time to first meaningful prediction and observation: ___

Which command, term, or evidence selection caused avoidable friction? ___

## Learning and Engagement

| Learner label | Opening diagnostic | First rubric score | Revised score | Individual exit explanation | Wanted to know what happened (1–5) | Manageable challenge (1–5) |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

Targets: first observation within 15 minutes; 360 teaching minutes; at least
210 active minutes; 80% at 6/8 with no zero after one revision; median 4/5 on
both feedback questions. Keep individual and group results distinct.
The rubric target measures improvement after review; it is separate from
[independent course completion](../agenda.md#completion-and-feedback). Record
worked reveals and the exported completion fields alongside the rubric scores.

Ask each learner what dragged and where they needed more explanation. Compare
opening and exit answers by mechanism and evidence quality using equivalent,
different examples; a small pilot does not establish a general learning effect.

## Optional LLM Comparison

LLM support is experimental and disabled by default. Read the
[configuration and evaluation guide](../delivery/llm.md) before enabling a
feature. Begin with Challenge 5 review under facilitator observation. Complete
the synthetic calibration checks before using held-out examples. Suggested
expectations are not human annotations; record the facilitator's judgment.

Compare static hints/self-review with requested LLM advice using equivalent
tasks and the same rubric. Record prior experience, support exposure, and model
assignment. A small pilot supports a revision decision, not a general effect
estimate. Preserve enough unseen equivalent problems for later unassisted
assessment; do not use the same exposed answer as a transfer measure.

For an initial supervised trial, inspect the generated advice with the learner
before they act on it. Advice delivered by the runner is already recorded as
answer-bearing help. If a facilitator shares advice generated elsewhere,
record equivalent support exposure before any reassessment; do not count that
learner's response as unassisted. No LLM advice is available during the exit.

| Learner / task | Static or LLM support / feature | Model / server version / prompt version | Grounded feedback? | Facilitator correction / time | Revision / later fresh unassisted outcome |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

| Example / cited claim | Citation supports conclusion? | Useful revision question? | Uncertainty preserved? | Unsupported criticism or answer leakage? | Latency / token usage |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Record refusals, schema failures, bad citations, overly confident advice,
interruptions, and endpoint unavailability. Separate better writing and faster
completion from improved reasoning on fresh unassisted work. Save private
evaluation files under `work/llm-evals/`; report only appropriate aggregates.
Record whether the next decision is to revise prompts, test another model,
expand cautiously, or keep the static support path.

## Revision Decision

| Finding | Evidence | Change | Owner | Next validation |
| --- | --- | --- | --- | --- |
| | | | | |

If time overruns, shorten recognition tours or repeated reporting before
cutting investigation and debrief. If explanations are shallow, improve the
prompt or evidence selection before adding more topics or interface features.
