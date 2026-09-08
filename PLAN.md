# Plan: Improve the Bootcamp's Teaching Technique

Status: proposed implementation; this plan does not change delivery behavior.

Review baseline: `a7146d5`. The current course has 36 phases, 29 required
checkpoint occurrences, seven reviews, three artifact bundles, and 57 tests.
The preceding consistency changes clarified existing behavior. This plan
deliberately changes that behavior where it limits learning, especially
reassessment after help.

## Outcome and Constraints

Deliver a course that responds to mistakes, lets learners test decisions,
gradually removes guidance, and provides a fair way to demonstrate later
independent understanding. Preserve the networking scope and the
[agenda's eight teaching blocks](agenda.md#one-day-teaching-contract): 360
teaching minutes plus 60 minutes of breaks. Installation remains separate.

Keep the local Mac environment, terminal and JSON interfaces, existing saved
evidence, anonymous sessions, and three deliverable bundles. Use the Python
standard library and the existing workbenches. No hosted service, accounts,
AI grading, general adaptive-learning framework, or network emulator is needed.
Human judgment remains responsible for assessing open-ended reasoning.

## Coverage of the Seven Technique Gaps

| Gap | Implementation | Evidence of completion |
| --- | --- | --- |
| Help prevents later independent attainment | Worked example, supported practice, and fresh reassessment with separate attempt histories | A revealed original answer stays exposed while a different unassisted problem can satisfy the same objective |
| Feedback does not diagnose errors | Rule-based misconception feedback and semantic parsing of factual answers | Missing headers, wrong units, and wrong route-selection rules produce different useful feedback |
| Guidance does not adapt or withdraw | Short support routes, targeted practice, and neutral capstone prompts | Novice and successful learners receive appropriate support without extending the block; first diagnoses precede leading questions |
| Choices do not affect observations | Bounded experiments using the existing networking models | A learner changes one permitted condition, predicts its effect, and compares a computed result |
| Reasoning review lacks support | Rubric calibration and a guided claim/evidence/limitation/next-test review | Learners assess an example before self-review; reasoning remains distinct from structural validity |
| Recording and review create friction | Submit artifact sections directly, record each answer once, and scope review hashes to assessed content | No repeated paragraph entry; unrelated edits preserve earlier reviews |
| Technique has not been tested with learners | Observed pilots, comparable unseen tasks, and explicit revision decisions | Real observations are recorded separately from synthetic software journeys |

## 1. Define the Learning and Assessment Contract

Extend [delivery/course.json](delivery/course.json) with stable objective IDs,
problem-family IDs, artifact bindings, support references, and assessment roles.
Keep the eight blocks as the fixed backbone. Support and reassessment are small
activities within a block, not a general graph of alternate courses.

Inventory all 29 existing checkpoint occurrences. Distinguish conceptual
assessment from recording requirements: a case ID, citation format, or selection
of two valid budget options still needs validation, but is not independently
evidence of networking understanding. Map every conceptual checkpoint to an
equivalent reassessment. Several checks may share a problem only when its
scoring explicitly covers every mapped objective. Do not silently drop checks.

Keep explanation review at the existing seven points and retain the four
0–2 rubric dimensions, the 6/8 threshold, and no-zero requirement. A correct
fact does not establish a correct explanation. Self-review and facilitator
review remain separate, unauthenticated local records.

Replace the permanent completion barrier with these explicit rules:

- Original attempts, hints, worked reveals, corrections, and skips remain in
  history. A revealed answer never becomes independent by being re-entered.
- An objective can be satisfied by a qualifying original response or a correct
  unassisted response to a fresh, equivalent problem. Required explanation
  review must still pass against the relevant current work.
- A qualifying original response is the first committed correct assessment
  response before answer-bearing help or corrective feedback. Formative
  retries remain useful practice; they need a fresh problem for an independent
  result. Input-format errors do not consume an assessment attempt.
- A reassessment is fresh only if that learner has not seen its answer, worked
  explanation, or an earlier assessment of that variant. A shuffled question
  order alone is not a new problem.
- Asking for an answer-bearing hint during reassessment converts that attempt
  to supported practice without punishment; a different variant is needed for
  an independent result. Separate orientation help from answer-bearing help.
- An incorrect reassessment records the failed attempt before diagnostic
  feedback appears. Correcting it is useful practice, not a new independent
  assessment. Exhausted variants leave an explicit unmet objective.
- Completing activities, recording required work, satisfying objectives, and
  obtaining current self/facilitator reviews remain separate outcomes. A
  corrected supported attempt counts as recorded work; it does not alone
  satisfy an objective. Unresolved skips, missing artifacts, or failed reviews
  still prevent the corresponding completion claim.

Version the changed state and JSON contracts explicitly. Preserve existing
navigation commands and valid local exports. Existing sessions must not be
silently regraded, migrated, or reset: document using their matching course
copy to resume/export, and starting the new course separately. Update the
agenda, student briefs, facilitator guide, and delivery contract together.

## 2. Build the Transfer Challenge as the First Complete Slice

Implement the new learning loop in Challenge 2 before extending its structures
to the entire course. Reuse [delivery.py](delivery.py), its atomic persistence,
revision checks, and the existing pure workbench evaluation functions.

Add one small, versioned problem catalog under `delivery/`. Prefer a finite
authored set with validated parameters over unrestricted random generation.
Give each problem an objective mapping, variant ID, declared conditions,
evidence provenance, supported-use eligibility, scoring rules, and worked
explanation. Keep answer keys out of pre-attempt status and learner exports.

For the transfer slice, author a supported problem and at least two alternative
reassessment variants. Vary the path limit and declared header overhead while
preserving the same reasoning demand. Include at least one example where the
small transfer fits. Check arithmetic bounds and avoid implying that a size
calculation proves feedback delivery or application recovery.

Record problem ID, parameters, presentation time, exposure, first response,
corrections, feedback category, and assessment result. Store the assigned
variant before presenting it so reconnects and repeated requests cannot reroll
the problem. The same seed and history must reproduce the same assignment.

Expose typed actions for requesting support, submitting a problem response,
and requesting reassessment through both terminal and JSON delivery. Action
names and payloads must be documented before expanding the first slice. Keep
all mutations behind the existing revision and request-ID checks.

Acceptance for this slice: a learner answers incorrectly, receives targeted
feedback, opens a worked explanation, completes supported practice, quits,
resumes on the same pending fresh variant, and independently passes it. The
original remains exposed, the objective becomes satisfied by the fresh result,
and overall completion still requires the remaining work and reviews.

## 3. Diagnose Mistakes and Target Support

Replace the generic wrong-answer response with a bounded set of authored
misconception rules. Return structured result codes alongside plain-language
feedback and a relevant evidence field or next question. Unknown mistakes
receive honest general guidance, not an invented diagnosis.

Examples to implement and test:

| Response or reasoning error | Feedback target |
| --- | --- |
| MTU used as payload | Distinguish IP packet length from TCP data length |
| Only one header subtracted | Identify both specified headers |
| Correct number expressed in bits | Distinguish bytes from bits before recalculating |
| Lower preference chosen over a longer prefix | Apply prefix length before preference/metric |
| Recorded convergence interval treated as application recovery | Identify what the final recorded event actually measures |
| Intended policy treated as observed enforcement | Request an actual rule, session, or packet observation |
| UTC offset applied in the wrong direction | Establish the same instant in both representations |

Parse quantities, units, IP addresses, prefixes, and unordered next-hop sets
semantically where appropriate. Use standard-library parsers and explicit
units; do not equate lowercase `b` with uppercase `B` by normalizing them first.
Accept equivalent representations without weakening the underlying check.
Malformed input remains distinct from a valid but incorrect response.

Do not attempt to infer arbitrary prose meaning with string matching. Ask a
structured follow-up for diagnosable distinctions, then leave the explanation
to the rubric. Preserve the existing workbench CLI behavior while sharing
evaluation rules with guided delivery.

Use objective and misconception results to recommend a short existing
reference fragment or practice problem. A successful response can bypass that
support. Repeated difficulty offers a worked example and fresh reassessment.
Optional practice should target the demonstrated need instead of always taking
five randomly ordered questions. Record the recommendation, learner choice,
and outcome; do not infer ability from speed alone.
Bypassing optional support must not skip required investigations, explanations,
or the individual exit.

Extend reviewed variants and feedback to foundations, prefix/VRF lookup,
convergence and policy choice, cloud return paths, and timestamp/evidence
interpretation. Maintain a complete mapping from the original conceptual
checks before switching the entire course to objective-based completion.

## 4. Remove Leading Prompts as Guidance Withdraws

Keep explicit modeling and copyable commands early in the day. Later blocks
should ask learners to select evidence and justify the next check. Support
remains available on request, with its effect on assessment recorded.

Change the capstone and individual exit to this order:

1. Present a neutral symptom, service requirement, and initial context.
2. Record an initial diagnosis or competing hypotheses, confidence, and the
   next evidence request before displaying diagnostic checkpoint wording.
3. Let the learner inspect permitted evidence in a chosen order and explain
   what changed in the claim.
4. Collect neutral structured facts and the revised explanation for review.
5. Offer targeted questions and worked review after that attempt.

Remove prompts such as “What exact return-route prefix was removed?” from the
independent stage. Ask which change matters and what evidence discriminates
between explanations. Audit prompt text, filenames, titles, evidence menus,
and JSON fields for premature diagnosis cues. Retain direct file access as a
teaching convention, not an exam-security boundary.

Keep main and exit assignments distinct for A/B and B/A. New reassessment
variants must not consume or expose the reserved exit case. Review variants
for comparable reasoning demands; changing names alone is insufficient, and
adding unrelated protocol knowledge would violate scope.

## 5. Make Decisions Produce Bounded Model Results

Add three controlled experiment families using existing calculations and
fixtures. These are explicit models of the supplied scenarios, not live
configuration or claims about unobserved devices.

| Experiment | Permitted change | Result to compare with a prediction |
| --- | --- | --- |
| Transfer | Select a supplied payload size or header-overhead condition | Whether the packet fits the declared path limit and the limiting calculation |
| Routing | Remove one eligible route or select a supplied lookup context | Winning prefix, eligible next hops, or no matching route |
| Resilience | Choose two existing improvements and an authored failure condition | Which stated failure effects the modeled changes address and which dependencies remain |

Require a saved prediction before releasing each result. Include parameters,
baseline evidence version, model version, and variant ID in the result. Keep
baseline evidence immutable; derived results and learner choices stay under
the session workspace. Do not represent generated results as new sensor logs.

Use fixed parameter schemas and pure functions. No arbitrary shell, filters,
paths, network access, device changes, or dynamic code evaluation. Reuse the
route-selection functions and arithmetic already in the repository. For the
resilience exercise, state assumptions explicitly: no token purchase guarantees
real failover, and an unknown remains unknown when the model lacks evidence.

Connect token choices to those results instead of revealing the same outcome
for every selection. Ask learners to revise one choice after the shared-power
condition, preserving the original decision and its rationale. Keep narrative
quality outside the automatic score.

## 6. Support Reasoning Review and Reduce Recording Work

### Calibrate the Reviewer

Turn the existing graded examples into a short activity before the first
self-review. Learners score two concise responses, see the authored scores
and rationale, and compare one disagreement. Use the same four rubric
dimensions throughout. Calibration is formative, not another completion gate.

At each review, guide the learner or facilitator through one representative
claim, its cited record, its limitation or alternative, and the next test.
Show relevant rubric anchors next to the work and ask for a concrete revision
when a dimension is weak. Preserve first and revised scores. Automate missing
references and fields, but never claim those checks prove the reasoning sound.

### Enter Each Answer Once

Keep Markdown/CSV as the authoritative long-form work. Bind response regions
to stable IDs so visual heading edits need not determine identity. Use a small
set of explicit markers in the three templates, not a general document format.
Reject missing or duplicate required markers with a precise recovery message.

Add a submit-from-artifact action that reads the bound region, checks the
expected content hash, and snapshots it into existing submission history.
Terminal learners edit that region once and submit it without retyping the
paragraph. Keep short factual answers in session state once; remove duplicate
transcription requirements from templates and include those results beside
their explanation in exports. Existing direct JSON answer submission remains
available to clients that manage their own input.

Do not automatically rewrite a learner-edited artifact. This design avoids
making a state file and editable document competing authorities or requiring
a new multi-file transaction system. History snapshots remain assessment
evidence; they are not another place the learner must edit.

Present the current prompt, selected evidence, relevant artifact region,
outstanding checks, and next action together in the terminal. Preserve the
plain-text and headless paths. A browser interface is not required to eliminate
duplicate entry and unnecessary navigation.

### Invalidate Only Affected Reviews

Replace whole-artifact review hashes with hashes of the assessed regions,
relevant ledger records, and submitted responses. Include all dependencies
that the review actually assesses: an integrated capstone review may correctly
depend on several artifacts, while a packet-path review should not depend on
an unrelated later exit note. Declare these dependencies explicitly.

Normalize line endings only; do not erase substantive edits through loose
normalization. Use stable evidence IDs for ledger rows. Adding an unrelated
row or editing another region should not invalidate earlier work, while
changing or deleting a cited record must. Display which reviewed content
changed and preserve the original snapshot for comparison.

## 7. Fit the Technique Changes Into Six Teaching Hours

These allocations replace portions of existing activities. They are not extra
time added to the agenda. The exact phase count can change; update code,
documentation, exports, and verification together instead of hardcoding 36.

| Block | Minutes | Allocation |
| --- | ---: | --- |
| Opening | 15 | Prediction 5; diagnostic 5; first observation and brief rubric calibration 5 |
| Packet | 65 | Model 10; inspect 25; varied lookup/support slot 20; review 10 |
| Transfer | 45 | Hypotheses 5; inspect 15; experiment/support/reassessment slot 15; review 10 |
| Routing | 40 | Predict 5; reconstruction with targeted support 15; compare contexts 10; review 10 |
| Resilience | 60 | Requirements 10; flows 15; choices, experiments, and twist 20; review 15 |
| Incident | 65 | Predict 5; three rounds of 12; narrative 14; review 10 |
| Capstone | 55 | Independent framing 5; investigation 20; handoff 10; exchange 10; review 10 |
| Individual exit | 15 | Unseen response 5; review/revision 5; feedback 5 |
| **Total** | **360** | **Breaks remain 15 + 30 + 15 minutes** |

Within a support slot, choose a supported or less-guided path; do not run both
complete paths serially. Budget at most one support/reassessment cycle per
objective family during the day. Additional practice or a second fresh test is
optional continuation after class. Report unmet objectives honestly rather
than promising that every learner attains them within six hours.

Protect evidence inspection, the individual exit, and breaks. Preserve at least
210 planned active minutes and mark planned versus observed time separately.
Timers remain advisory. If the first pilot overruns, reduce repeated reporting
and optional repetitions before removing investigation or feedback.

## 8. Validate the Technique With Actual Learners

Extend [facilitator/pilot.md](facilitator/pilot.md) to record what prompted
support, whether feedback resolved the misconception, the next evidence a
learner chose, whether the first diagnosis preceded a cue, and whether a fresh
problem was solved without answer-bearing help. Keep confidence before and
after evidence separate from correctness and reviewer judgment.

Start with observed transfer-slice sessions involving a beginner and an
experienced learner. After repairing obvious friction, run at least one full
beginner-solo pilot and one paired pilot with separate individual exits.
Participants and facilitator availability are human dependencies; do not
replace them with simulated learners or initiate recruitment messages without
the user's authorization.

Use comparable authored examples for an initial and later assessment of the
same objective. Record prior exposure and support. Include an unseen use of
an earlier idea near the end of the existing day to examine transfer beyond
immediate correction. Compare first attempts, supported corrections, and fresh
unassisted results separately; do not count retries as additional learners.

Have a facilitator review the same selected work as the learner and record
rubric disagreements. Preserve the existing pilot targets: first meaningful
observation within 15 minutes, 360 teaching minutes, at least 210 active
minutes, 80% reaching the rubric threshold after revision, and median 4/5 on
both engagement questions. Independent reassessment is an additional measured
outcome, not something implied by the rubric target.

Export local per-objective attempts, support levels, variant IDs, error codes,
review revisions, and optional feedback. Free text remains excluded by default.
Self-reported duration, process timestamps, and observed active minutes must
remain distinct. A worksheet and local summary are sufficient; no analytics
service or cohort dashboard is needed.

For every observed failure, record the evidence, proposed teaching or interface
change, owner, and next validation. Report participant counts and raw outcomes;
this small pilot supports iteration, not a general claim of learning efficacy.

## Implementation Sequence and Commit Boundaries

Complete and verify each increment before the next, using one-line commit
messages. Do not switch the default course to partially mapped assessment
rules. Temporary unfinished activities must be explicit in development state
and rejected by final verification.

1. **Define contracts and timing.** Inventory checkpoints, objective mappings,
   variants, review dependencies, version changes, and the block budget. Update
   the proposed delivery contract and add validation for the new definition.
   Commit: `Define learning objectives and reassessment contracts`.
2. **Finish the transfer slice.** Implement semantic feedback, supported
   practice, durable variant assignment, and fresh reassessment through both
   interfaces. Prove the complete help-to-reassessment journey.
   Commit: `Add targeted feedback and fresh transfer reassessment`.
3. **Extend support and withdraw cues.** Cover every remaining objective family,
   target practice to errors, and make capstone/exit investigation begin with
   a neutral prompt. Switch completion only after all mappings are implemented.
   Commit: `Adapt support and remove leading assessment prompts`.
4. **Make experiments consequential.** Deliver transfer, routing, and resilience
   experiments with prediction-first results and immutable baseline evidence.
   Commit: `Connect learner decisions to bounded model results`.
5. **Improve work capture and review.** Bind artifact regions, add direct
   submission, calibration, guided review, and dependency-scoped snapshots.
   Commit: `Reduce duplicate work and focus rubric review`.
6. **Rehearse and prepare the pilot.** Finish failure-path checks, update all
   teaching and automation documentation, verify timing on every supported
   route, test the distributable archive, and prepare observation/export forms.
   Commit: `Verify learning journeys and prepare observed pilots`.
7. **Observe and revise.** Run the real learner pilots when participants are
   available. Keep individual raw records under ignored `work/`; commit only
   an appropriate aggregate validation record and resulting course changes.
   Commit: `Record learner pilot findings and refine delivery`.

Primary implementation locations are [delivery.py](delivery.py),
[course.py](course.py), [the course definition](delivery/course.json), the
three workbenches, challenge fragments and templates, and existing tests and
verification scripts. Keep prose in Markdown and rules in a small explicit
catalog; extract helpers only when shared logic justifies them.

## Acceptance Checks

Use the existing standard-library suite and extend its behavioral journeys.
Do not add tests that merely assert the wording of the implementation.

- A worked reveal followed by a correct known answer remains supported. A
  genuinely fresh unassisted variant can satisfy the mapped objective without
  deleting that history. A failed, hinted, or exhausted reassessment cannot.
- Every required conceptual checkpoint has a tested equivalent reassessment;
  recording-only requirements remain validated. Completion cannot be gained
  by an unrelated successful problem or a passing rubric score alone.
- Wrong units, missing headers, incorrect route precedence, and unsupported
  causal claims receive appropriate distinct feedback where rules exist.
  Equivalent valid inputs pass, and unknown errors do not receive fabricated
  explanations.
- Status, help, errors, and evidence menus do not leak reassessment answers or
  leading capstone prompts before the first attempt. Both A/B and B/A preserve
  the reserved case. Support remains available with accurate exposure records.
- Novice, successful, and repeatedly struggling journeys choose the intended
  bounded support routes. Session restart, retry, and concurrent requests do
  not change an assigned variant, duplicate advancement, or erase attempts.
- Each experiment changes only permitted parameters and produces independently
  checked results. Predictions precede result release; malformed parameters,
  tool failures, and interruption preserve prior work. Baseline hashes remain
  unchanged, and generated evidence is clearly identified as model output.
- A learner submits long-form work once. Missing regions, malformed CSV,
  external edits during submission, invalid paths, and conflicting revisions
  fail clearly without overwriting work. Exports contain matching reviewed
  content and omit free text unless explicitly requested.
- Unrelated artifact edits preserve reviews; relevant text, checkpoint results,
  or evidence changes invalidate all affected reviews and identify the reason.
  Calibration completion cannot substitute for a review of the learner's work.
- All supported in-class routes fit the allocated blocks and preserve 360
  teaching minutes plus 60 break minutes. Unfinished attainment and optional
  after-class work are explicit. Synthetic timings are not learner timings.
- Existing navigation and workbench commands still work. Version conflicts,
  corrupt state, old exports, package extraction without Git metadata, and
  documented recovery are checked without migrating old results silently.
- CI runs the portable contracts and real-tool Mac journeys. Markdown lint,
  local links, fragment references, evidence commands, and documentation of
  assessment semantics agree with the final implementation.

Reproduce the main technical checks with the existing commands, extended for
the new journeys:

```sh
python3 -B -m unittest discover -s tests -v
./course verify
python3 -B verification/check_delivery.py --smoke --journey
markdownlint-cli2 "**/*.md"
git diff --check
python3 -B verification/package_course.py --output work/course-technique.tar.gz --journey
```

Stage new intended source files before packaging and choose an unused output
filename. Do not publish the archive or include learner work.

## Definition of Done

Implementation is complete when all seven gaps have functioning support in the
course, automated checks pass, the documentation describes the new assessment
rules consistently, and the real-learner pilot workflow is ready. Report that
milestone as implementation complete with learner validation pending if no
participants are available.

The teaching technique is validated only after the specified learner pilots
have been observed, findings recorded, and material issues addressed or
explicitly retained for another trial. Do not mark the pilot step complete
based on scripted journeys. Preserve that outstanding work in the validation
record if this implementation plan is later removed at the user's request.
