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
work; create a separate session for the new course. Default exports omit learner
answers, artifact text, and generated advice. JSON summaries still include
computed experiment results and calibration feedback. The local course remains
an open learning environment, not an exam security boundary.

Support replaces part of the current block's practice time: one support and
reassessment cycle per family during class, another fresh attempt optionally
after class. No claim of guaranteed six-hour mastery follows from the schedule.

## Outcome and Review Map

The opening is formative: it records starting knowledge without a rubric
grade. Its subnet and service-boundary objectives still need later independent
demonstration if unmet. Revisit `opening.diagnostic` for fresh family tasks;
correcting the diagnostic preserves its original history.

| Outcome | Factual evidence | Artifact region and review anchor |
| --- | --- | --- |
| Local delivery and service boundaries | `opening.local`, `opening.dns`, `opening.application` in `opening.diagnostic` | `packet-path.md:c01`: distinguish peer/gateway MAC from destination IP and cite the observed trunk |
| Route selection and path change | Four route checks in `c01.change` | `packet-path.md:c01`: explain specificity, candidate ties, and unknown actual ECMP member |
| Packet size and diagnosis | `transfer.payload` in `c02.calculate` | `packet-path.md:c02`: account for headers and distinguish observed ICMP from endpoint receipt |
| Routing recovery and isolation | Convergence checks in `c03.reconstruct`; BGP/VRF checks in `c03.compare` | `packet-path.md:c03`: distinguish forwarding installation from application recovery; respect the context |
| Architecture and policy | Cloud/policy checks in `c04.flows`; budget recording in `c04.choose` | `architecture.md:c04,budget`: trace both directions; intended permit is not route availability or session success |
| Qualified investigation | UTC and auth-record checks in `c05.round2` | `incident.md:c05` plus ledger: process-to-DNS is not process-to-socket; TShark and Zeek can share a source; successful authentication does not prove credential theft |
| Defensible handoff and fresh diagnosis | Case/change/lookup/observation in `c06.analyze` and `exit.answer` | `c06-path`, `c06-architecture`, `c06-handoff`, then `incident.md:exit`: connect action to decisive evidence, operational effect, owner, validation, and rollback |

Seven existing reviews (`c01` through `c06`, plus exit) cover these anchors.
For **mechanism**, 2 means the applicable rule and path are correct, 1 means
incomplete explanation, and 0 means a central contradiction. For **evidence**,
2 cites the decisive record and its collection limit, 1 supplies a relevant
but incomplete citation, and 0 has no support or invents a record. For
**uncertainty**, 2 names a material alternative and discriminating check, 1
merely lists an unknown, and 0 treats an unsupported claim as fact. For
**action**, 2 supplies an evidence-linked next step with owner and success
condition (plus rollback for a change), 1 is useful but incomplete, and 0
is unsupported or ignores the stated service dependency. Cite the learner's
passage when assigning each score; these anchors do not automate prose grading.

IPv6, STP/LACP, FHRP, VPN, MPLS/SD-WAN, fabric/overlay vocabulary, and ATT&CK
are recognition references. Their configuration skills are not completion
requirements. The [family prompts](problems.json) state prerequisites for
every fresh task. Required subnet membership stays at `/24`; route exercises
with less familiar boundaries supply address ranges so they assess selection.

## Worked Learner Journey

1. The learner answers a subnet diagnostic incorrectly. Save that first
   answer and outcome; it does not become correct retroactively.
2. They request worked subnet support and explain the completed example.
   Record supported practice and exposure, with no rubric point deduction.
3. They request an unseen subnet reassessment and answer correctly on the
   first unassisted attempt. That objective now has independent evidence.
4. They revise the packet explanation to distinguish IP and next-hop MAC,
   then submit the current artifact region. The revision remains visible.
5. A reviewer cites that current text and records, for example, 2/2/1/1.
   This passes 6/8 with no zero, while the feedback identifies a better
   uncertainty check and action. Other unmet objectives still remain unmet.

Manual facilitation uses the same record: learner label, objective, task ID,
first answer, support/exposure before answer, result, fresh task ID, artifact
revision, reviewer, four scores, and cited feedback. Preserve earlier rows.
Do not convert partner help or an exposed retry into independent attainment.
Self review and facilitator review remain different judgments.

Exit timing is still a pilot question. Observe instruction, navigation,
analysis, and writing separately. A documented pilot may move five minutes
from the capstone exchange to the exit answer, retaining a peer handoff and
the combined 70 minutes. The published schedule stays unchanged until learner
evidence supports that substitution.

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
Supported corrections count as recorded work. Default JSON exports include
result categories and parameters without learner answers or unshown
reassessment keys.

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
Default JSON exports contain help metadata; explicit JSON/Markdown artifact
exports include private advice and context. LLM histories are separate from
self/facilitator review histories and never represent authenticated external
assessment.
