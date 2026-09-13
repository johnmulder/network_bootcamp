# Learning and Reassessment Contract

Learning contract version 2 remains active. Course, state, and JSON protocol
version 3 add optional advisory LLM actions. Every conceptual checkpoint has
an executable reassessment.

Every checkpoint occurrence has a stable objective, problem family, scoring
field, and support reference in `course.json`. Case IDs, original record numbers,
and two valid budget selections are recording checks. All other checkpoints
assess concepts. Artifact bindings identify the sections containing explanations.
The seven rubric reviews still assess mechanism, evidence, uncertainty, and
action on 0–2 scales; passing requires at least 6/8 and no zero.

An objective requires a correct first committed response before corrective
feedback or answer-bearing help, or a correct unassisted first response to a
fresh equivalent problem. Invalid input formats do not consume an attempt.
Corrections and supported practice remain useful recorded work. Neither erases
the original attempt or turns an exposed answer into independent evidence.

Problem assignment is a durable action, using the session seed and prior variant
history. Reconnecting, repeating a request, and retrying the same problem cannot
produce a fresh attempt. Each finite family has a supported example and at least
two reassessment variants. Requesting answer-bearing help converts that attempt
to practice. Exhaustion reports an unmet objective. Orientation help never
supplies answers. Family-specific support and model results expose only the
related original checks; general block hints and reveals can expose all of
that block's unfinished checks. Independent success does not waive
investigations, explanations,
the individual exit, or reviews.

Delivery finished, required work recorded, objectives satisfied, self-reviewed
completion, and facilitator-reviewed completion are separate outcomes. Supported
corrections count toward recorded work. Self and facilitator reviews are separate
unauthenticated local judgments; no automated prose grading is introduced.

State and JSON protocol version 3 reject older sessions without migration,
reset, or regrading. Use the matching older course copy to resume or export old
work; create a separate session for the new course. Default exports omit prose
and answer keys. The local course remains an open learning environment, not an
exam security boundary.

Support replaces part of the current block's practice time: one support and
reassessment cycle per family during class, another fresh attempt optionally
after class. No claim of guaranteed six-hour mastery follows from the schedule.

## Typed Learning Actions

All conceptual checkpoint phases implement these operations.
They use the existing request ID, revision, phase ID, action, and payload envelope.
Assign a problem in its checkpoint phase; revisit that released phase later if
needed. Assignment is saved before the prompt is returned. Status includes
assigned prompts and attempt counts, never pre-attempt keys.

| Action | Payload | Effect |
| --- | --- | --- |
| `support` | `family`, `level`: `orientation`, `practice`, or `worked` | Orientation gives process help; practice assigns a supported variant; worked shows that variant's explanation |
| `reassess` | `family` | Assigns an unseen assessment variant or reports exhaustion |
| `problem_answer` | `variant_id`, `answers` keyed by displayed question IDs | Records factual results; only a first unassisted correct assessment qualifies |
| `problem_hint` | `variant_id` | Shows worked reasoning and permanently marks that variant exposed |

Terminal keys are `u` for support, `n` for reassessment, `b` to answer the assigned
problem, and `j` for its answer-bearing help. An unfinished assignment is returned
again instead of rerolled. A repeated request ID returns its saved result.
Supported corrections count as recorded work; default exports include result
categories and parameters without learner answers or authored keys.

## Optional LLM Advice

The [LLM support guide](llm.md) defines configuration and explicit review,
coaching, and handoff actions. These features are disabled by default and are
never completion requirements. No LLM advice is available for the independent
exit. Model output cannot supply a rubric score, edit a submission, advance a
phase, or change the deterministic factual result.

Delivered advice is answer-bearing help. Coaching requires a committed answer
and exposes only its current family; review and handoff advice expose their
block. Existing independent outcomes are preserved, and unfinished assigned
reassessments in that scope become exposed practice. Fresh unassisted outcomes
remain governed by the finite authored catalog.

Advice and exposure are committed together before delivery. Pending, failed,
cancelled, and stale advice do not consume an independent attempt. A lost
response after commit retains exposure and replays the same saved advice.
Default exports contain help metadata; explicit artifact exports include the
private advice and context. LLM histories are separate from self/facilitator
review histories and never represent authenticated external assessment.
