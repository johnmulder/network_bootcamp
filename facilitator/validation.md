# Implementation Validation

The current curriculum is version 3.1; the session protocol remains 3 and the
learning contract remains 2. Older sections retain historical checks; their
counts describe those snapshots. No software check establishes learner
attainment or an observed class duration.

## Curriculum 3.1 Readiness — September 16, 2026

### Implemented Changes

- Corrected nested-route selection, IPv6 on-link information, STP terminology,
  virtual gateway takeover, and claims about policy, TLS, and authentication.
- Taught the assessed `/24` method, aligned all required subnet variants, added
  row/JSON reading examples, and mapped outcomes to exact review anchors.
- Mapped all 104 guides to tasks, evidence, and completion criteria. Missing
  device state is explicitly unknown or a stated conceptual exercise.
- Added DNS/attachment comparisons, saved performance measurements, and a
  separately hypothetical recovery epilogue. The required day still has 36
  phases and 360 teaching minutes; fuller comparisons are optional.
- Added 23 Mermaid figures, text equivalents, and 46 light/dark SVG exports.
  The [diagram record](../diagrams/README.md#visual-review-record) describes
  actual rendering QA. A scenario index distinguishes snapshots and aliases.
- Added three pinned Wireshark packet exemplars, public test keys, source
  notices, offline hashes, reproducible curl acquisition, and frame assertions.
  These optional lessons do not add a learner runtime or contact trace hosts.

New sessions are required: assessed content and generated fixture fingerprints
changed. Retain matching 3.0 copies for old sessions; no migration or regrading
is implied. The baseline used for this audit is commit `a138967`.

### Completed Technical Checks

Validated implementation: `d5ff2d5`, on macOS with Python 3.13.15,
TShark 4.4.1, and jq 1.8.2. These are local checks, not a remote CI run.

- All **123 standard-library tests passed**. The new acquisition tests reject
  changed bytes, HTML, HTTP failures, and missing companions while preserving
  existing assets. Provider tests use simulated responses.
- Course verification passed: 39 generated fixtures, five upstream assets
  comprising three captures, one test key log, and one license notice,
  83 workbench questions, 17 timeline events, and 36 phases / 360 minutes.
- All 32 real-tool evidence views and both complete A/B and B/A fresh-process
  journeys passed. Responses and rubric scores are synthetic; they are not
  learner outcomes. One earlier rehearsal correctly rejected a session after
  the course version changed during the run; both fresh 3.1 journeys passed.
- All 104 reference guides have evidence-matrix coverage; all 36 distinct
  documented evidence commands ran successfully. Public-capture protocol and
  exact-frame assertions passed with the pinned bytes and public test keys.
- All 23 Mermaid sources match their 46 rendered exports. Every export was
  visually inspected in light/dark contact sheets; automated browser checks
  found titles, descriptions, and no text outside the SVG canvas.
- All 24 Python files parse with Python 3.10 syntax rules. Markdown lint,
  local links/anchors, offline LLM inventories, and Git whitespace checks
  passed. Optional Zeek and iperf3 were unavailable and were not exercised.

The local archive `work/implementation/network-bootcamp-3.1.tar.gz` contains
267 tracked files plus `RELEASE.json`. It passed verification, reference and
packet decoding checks, doctor, all views, and both full journeys after
extraction to a path containing spaces, without Git metadata. LLM settings
and credentials were removed from its child environment; no asset fetch or
diagram rendering occurred. Separate portable checks passed with TShark, jq,
Git, and Node absent from PATH. Learner work and this implementation plan are
excluded. This result summary was added after the archive was built.

Archive SHA-256:

```text
344fd30529fcdf1ebbf50243da8e3191f620f55148466aed8d43592a07fcf2fb
```

### Human Validation and Revision Decision

Observed learners: **0**. Independent human technical reviewers: **0** for
this revision. Timing, active minutes, fresh attainment, delayed outcomes, and
both engagement ratings are **unmeasured**, not zero-valued results. No model
or automated rehearsal substitutes for a participant or second reviewer.

| Remaining gate | Required evidence | Owner / next decision |
| --- | --- | --- |
| Beginner foundations and beginner/experienced transfer slices | Anonymous first attempts, support exposure, fresh equivalents, instruction/navigation/analysis/writing time | Facilitator: repair blocking instructions before full days |
| Illustration comparison and evidence-choice trial | Prior experience, assigned version, observed interpretation, changed claim/action | Facilitator: retain or revise explanations from actual observations |
| Beginner solo and paired days with individual exits | Individual counts, observed active minutes, rubric revisions, feedback, exit timing | Maintainer: revise allocations or narrow the six-hour novice claim if targets fail |
| Independent technical and rubric review | Sources/records checked, independently scored sample, reconciled disagreements | Second reviewer: approve corrections or identify concrete revisions |
| Optional delayed fresh follow-up | Interval, unseen variant, exposure, missing follow-ups | Facilitator: report retention separately from immediate transfer |

Use the [updated pilot worksheet](pilot.md#curriculum-31-trials) with LLM
support disabled. Keep private raw work in ignored `work/`. Commit aggregate
counts and revision decisions after observation; use learners as denominators,
not attempts or pair submissions. Existing targets remain first observation
within 15 minutes, 360 teaching minutes, at least 210 active minutes, 80% at
6/8 with no zero after revision, and median 4/5 on both feedback questions.

**Decision:** ready for supervised curriculum trials after technical checks;
not yet validated for novice timing, independent attainment, or engagement.
Retain the published schedule until observed trials justify a change. The
five-to-ten-minute exit alternative is a documented trial, not a new promise.
Preparation of these worksheets does not complete the human validation gates.

## Expanded Local Evaluation and Learner Interface

The [second local evaluation](local-model-expanded-validation.md) records 190
attempts against the supplied local setup, including a connection failure
inside the sandbox. Of 189 provider responses, 188 passed local output
validation. All 80 held-out responses were accepted, but content errors remained.
Coaching now preserves deterministic factual feedback; the model contributes
the guiding question. Review, handoff, and authoring remain experimental.

The learner terminal presents readable advice, readiness and recovery guidance,
local-only history, and handoff context. All 118 tests passed, including 43
focused LLM tests. Course verification, all 31 real-tool views, and both full
case journeys passed. Saved-session replay made no additional inference calls.
Facilitator approval and learner trials remain pending. All features remain
optional and disabled by default, with configurable endpoint, model, and key.

## Initial Local Model Support

Optional schema-constrained output, compact context, and a configurable input
budget are implemented. The [local model evaluation](local-model-validation.md)
records actual LM Studio configuration, calibration, and live outcomes.
Model-specific observations do not establish learner benefit or qualify
other models. Older no-live-testing statements below describe earlier runs.

All 110 standard-library tests passed, including 35 focused LLM tests. Course
verification passed for 36 phases, 36 fixtures, 83 questions, and the 17-event
timeline. All 31 real-tool views and both full case journeys passed. The live
run made 68 calls; coaching and handoff are provisional starting features for
the tested local setup. Review and authoring remain unqualified. All features
remain disabled by default, with no hosted fallback or automatic retry.

## Documentation Audit Before Local Model Testing

The operational guides were checked against the current CLI, session/export
code, optional LLM context builder, setup script, and fixture/package tools.
Corrections cover the 31 evidence views, format-specific export contents,
private status responses, feature-specific LLM context, configuration limits,
request replay, and recovery using a matching course copy. Packaging uses Git
for its file list and the working tree for file contents.

Course verification passed for 36 fixtures, 83 questions, 36 phases, and the
17-event timeline. Temporary-session probes confirmed export privacy and
format differences; offline configuration probes confirmed endpoint path
restrictions. Markdown lint passed for 136 files, local link/anchor checks
passed for 248 links, and Git whitespace checks passed. Documentation edits
preserve the assessed-content fingerprint. This audit does not revalidate
every networking explanation in the reference
library. The 103-test run below was the latest full suite at that point;
live-provider qualification and learner validation were then pending.

## Course 3.0 Optional LLM Validation

The client, session actions, maintainer drafts, and synthetic evaluation
workflow are implemented. The complete course remains offline by default;
all four LLM features require explicit configuration and individual actions.
The [LLM guide](../delivery/llm.md) documents endpoint/key/model settings,
exposure rules, private exports, and interrupted-request recovery.

### Error-Handling Corrections

All three errors from the implementation review were reproduced before their
fixes. Seven new regression tests cover the corrected behavior:

- Guided delivery resumes with an interrupted request when LLM configuration
  is absent or invalid. Ordinary actions and explicit cancellation remain
  available without inference; saved answers and independent results survive.
- Plain and JSON-escaped copies of the configured API key are rejected across
  all four features. Tests exercise escaping in both response layers and
  verify that rejected advice reaches neither session exports nor draft files.
- Lone high and low Unicode surrogates are rejected before persistence.
  Requests finish as failed, with no advice or help exposure, and replay
  without another inference. Accented text and emoji round-trip unchanged
  through accepted advice, session storage, and artifact exports.

All 103 standard-library tests passed, including all 28 focused LLM tests.
Content checks passed for 36 phases and 31 evidence views; the ten synthetic
evaluation examples passed their offline inventory check. Markdown lint and
Git whitespace checks passed. Provider responses were mocked, with fake
credentials; no live-provider or learner validation was performed.

The course/state protocol remains version 3. Assessed-source edits change the
content fingerprint, so older sessions still require their matching course
copy. No session migration or regrading was introduced.

### Initial Implementation Checks

The following results describe the initial optional-LLM snapshot and archive,
before the error-handling corrections above.

Transport checks simulate OpenAI and LM Studio response formats, with local
authentication both off and on. Session checks cover phase/evidence limits,
scoped help, existing independent outcomes, fresh reassessment, concurrent
updates, stale advice, cancellation, replay without duplicate inference,
private exports, and terminal/JSON operation. Draft checks cover computed
conditions, private atomic output, confinement, and refusal to overwrite files.

- All 96 standard-library tests passed, including the complete offline course
  under a network-call trap. The ten synthetic LLM evaluation cases passed
  their offline inventory checks.
- Course checks passed for 36 phases, 31 evidence views, 36 evidence fixtures,
  83 workbench questions, and the 17-event timeline. All 31 real-tool views and
  both complete A/B and B/A course journeys passed. The journeys use synthetic
  responses and scores; they are not learner trials.
- All 17 Python files parsed using Python 3.10 syntax rules. Markdown lint,
  local links and anchors, content checks, and Git whitespace checks passed.
  No remote CI run is claimed.
- The local archive, `work/course-llm-v3-final.tar.gz`, passed verification,
  all real-tool views, and both complete journeys after extraction at a path
  containing spaces without Git metadata. Validation removed LLM configuration
  and credentials from the child environment. The archive excludes learner
  work and the implementation plan; its LLM configuration check reported all
  features disabled. This validation record was updated after that run.

### External Validation Pending at Initial Implementation

No API endpoint, model, or key was configured for that initial implementation.
No real OpenAI or LM Studio model was called in that run. Simulated transport
tests are not real-provider tests. Use `verification/check_llm.py --live` with
each selected model/server and record actual server versions, latency, usage,
schema failures, and facilitator judgments before recommending that setup.

The ten synthetic examples contain proposed expectations and separate
calibration/held-out splits. They have not been annotated by a facilitator.
No learner trial was performed, and no educational benefit is claimed. The
[LLM pilot comparison](pilot.md#optional-llm-comparison) records the remaining
human work. Preserve static hints, pair exchange, and self-review throughout.

## Course 2.0 Technique Checks

- All 75 standard-library tests passed. The 18 learning tests independently
  check every authored variant and objective mapping, semantic quantities and
  misconception codes, exposure and reassessment histories, invalid formats,
  variant exhaustion, concurrent assignment, corrupt learning history, bounded
  experiments, artifact submission, and scoped reviews. They also exercise
  terminal submission, edits during submission, neutral initial diagnoses,
  calibration, privacy for malformed references, and preservation of unrelated
  first attempts when targeted help is requested. Preflight rejects missing
  template bindings before a learner starts.
- The course retains 29 factual checkpoint occurrences: 25 conceptual
  objectives and four recording requirements. Eleven finite problem families
  provide 37 authored variants. Independent originals, supported corrections,
  and fresh reassessments remain separate. Seven human rubric reviews still
  require at least 6/8 and no zero, with separate self/facilitator records.
- Course verification passed for 36 unchanged evidence fixtures, 83 workbench
  questions, the 17-event incident timeline, and every required phase. The
  block budget remains 360 teaching minutes plus 15/30/15-minute breaks.
  The facilitator allocation of 265 active minutes is planned, not observed.
- All 31 registered evidence views ran with the installed Mac tools. Both
  A/B and B/A fresh-process journeys passed, including initial diagnosis gates,
  a wrong original followed by help and fresh reassessment, calibration,
  required experiments, submission from an artifact, review, privacy checks,
  and portable JSON and per-objective CSV exports. These use synthetic
  responses and scores and are explicitly not learner-pilot results.
- All 12 Python files parsed using Python 3.10 syntax rules. Markdown lint,
  local links/anchors, fragment/evidence-command checks, and Git whitespace
  checks passed. The existing CI jobs discover the expanded portable tests and
  run the updated Mac journeys; no remote CI run is claimed here.
- The [pilot worksheet](pilot.md) now specifies beginner and experienced
  transfer-slice observations, a full beginner solo day, and a paired day with
  separate exits. It records support triggers and outcomes, early and later
  confidence, cue exposure, chosen evidence, equivalent delayed problems,
  reviewer disagreements, and concrete revision decisions. Default exports
  exclude learner prose and distinguish attempts from participants.

The final local archive, `work/course-technique-final.tar.gz`, passed course
verification, all real-tool evidence views, and both complete journeys after
extraction at a path containing spaces without Git metadata. It excludes learner
work and the implementation plan. Its assessed-content and fixture fingerprints
match the final checkout; this validation record was updated after that run.

Final completeness review: all seven technique gaps have implementation support
and the pilot workflow is ready. Implementation is complete with learner
validation pending. The implementation plan can be removed while the outstanding
human work remains recorded below.

Assessed-content SHA-256 for the evaluated final archive:

```text
b878be01c387401977e8876906b36eec6f61c49808f657c916abb406a4272c80
```

### Human Validation Pending

Observed participants: **0**. No learner trial, engagement result, observed
active-minute total, or learning-effect estimate is claimed. Run the specified
pilots when participants and a facilitator are available, retain private raw
records under ignored `work/`, and commit only an appropriate aggregate and
resulting course revisions. Preserve first attempts, supported corrections,
and fresh unassisted outcomes separately; record any accidental cues and
unavailable fresh variants. Do not count scripted retries as learners.

The workflow is ready, but teaching validation requires observing the pilots,
addressing material findings, and recording the next trial decision. The targets
remain first observation within 15 minutes, 360 teaching minutes, at least 210
active minutes, 80% reaching the rubric threshold after revision, and median
4/5 on both engagement questions. None has been measured for this revision.

## Earlier Delivery Checks — September 5, 2026

- All 57 standard-library project tests passed. They cover the original
  navigator, fixtures, workbenches, and setup plus saved delivery, staged
  evidence, both case assignments, factual feedback, and rubric review.
- Failure tests cover duplicate/stale/concurrent requests, interrupted saves,
  corrupt state, changed content and fixtures, invalid JSON, paths and units,
  missing tools, command failures, timeouts, and output limits. Accepted work
  remains intact and execution errors are distinct from learning results.
- Artifact checks cover required fields and tables, the ten-field ledger,
  evidence references, timestamps, narrative limits, review hashes, and stale
  reviews. Export checks cover privacy defaults, explicit artifact inclusion,
  portable references, and rejection of overwrites and escaping paths.
- `./course verify` passed: 36 manifest-tracked evidence files, 83 workbench
  questions across three modules, the 17-event original timeline, and all
  36 delivery phases. Teaching totals 360 minutes, with 60 additional minutes
  for lunch and breaks.
- `./prerequisites/setup.sh --check` and `./course doctor --json` passed on
  the development Mac with Python 3.13.15, TShark 4.4.1, and jq 1.8.2. Readiness
  checks used existing tools without installing or rebuilding evidence.
  The ten Python sources also parsed using Python 3.10 syntax rules.
- All 25 registered read-only evidence views ran successfully using real
  tools. The content checker matched guided Markdown commands to those views
  and verified local document links and anchors.
- Fresh-process CLI journeys completed all 36 phases for A/B and B/A main/exit
  assignments, including a wrong answer, correction, quit/resume, an identical
  request retry, hints, a reveal, and revision of skipped work. Both journeys
  used synthetic artifacts and reviews, checked separate completion states,
  and read exported results after moving them. Evidence hashes were unchanged.
- The same real-tool smoke checks and both complete journeys passed inside a
  course archive extracted at a path containing spaces, without Git metadata.
  The archive contained saved fixtures and matching release fingerprints,
  preserved executable permissions, and excluded learner work and the plan.
- Terminal save/quit and default-menu routing are covered by tests; the
  terminal interface calls the same operations as the headless journeys.
- Markdown formatting, local links and anchors, and Git whitespace checks
  passed. The CI workflow parses with both portable and Mac delivery jobs.
  Those jobs are configured but have not been observed running on GitHub.

## Documentation Consistency Follow-Up — September 7, 2026

The agenda now defines one completion policy, linked from student, facilitator,
pilot, and delivery instructions. It distinguishes finished delivery, passing
rubric reviews, and independent completion, including corrections after worked
reveals. The opening lesson presents that distinction before learners choose
a reveal. Capstone instructions preserve the template headings and put the
case ID in its existing fields.

All six troubleshooting guides now describe the observed start of TCP closure
and the missing final server ACK. The architecture workbench and four related
guides distinguish intended permission from observed enforcement. The module
indexes identify the conceptual VXLAN/EVPN exception. Prerequisites link the
existing Zeek exercise and explicitly identify iperf3 as an extended tool with
no assigned course exercise.

After these documentation changes, all 57 tests passed, as did course
verification, all 25 real-tool evidence views, both complete fresh-process
journeys, Markdown lint for 134 files, local links/anchors, and Git whitespace
checks. The assessment code, fixtures, and schedule were unchanged. The archive
rehearsal above records the September 5 build; no replacement archive or remote
CI run was produced for this documentation follow-up. Learner-pilot validation
remains outstanding.

## Reproduce the Main Checks

Run from the repository root on a Mac with core tools installed:

```sh
./prerequisites/setup.sh --check
./course doctor --json
./course verify
python3 -B -m unittest discover -s tests -v
python3 -B verification/check_delivery.py --smoke --journey
markdownlint-cli2 "**/*.md"
git diff --check
```

Stage or commit the intended source files before packaging, and choose an
output filename that does not already exist:

```sh
python3 -B verification/package_course.py --output work/course.tar.gz --journey
```

The package command uses tracked files from the current checkout. Without
Mac tools, run the content checker without flags and package with `--check`
instead of `--journey`. See the [delivery guide](../delivery/README.md) for
request, recovery, review, and export contracts.

Markdown lint is a maintainer tool, not a student prerequisite. Optional
Zeek reference work uses `setup.sh --extended`, which also includes iperf3 for
self-directed experiments. Neither tool was installed or tested for this core
delivery validation, and there is no assigned iperf3 exercise. CI dependency
installation occurs before the offline course checks. No release was published.

## Learner Validation Still Needed

No real beginner, experienced-learner, or solo learner pilot was run during
implementation. No engagement scores, class completion times, or learning gains
are claimed. Automated journey responses and rubric scores are synthetic;
passing those checks establishes software behavior, not student attainment.

Use the [pilot worksheet](pilot.md) with actual learners for solo and paired
delivery, retaining separate individual exits. Measure the existing targets:
first observation within 15 minutes, six teaching hours, at least 210 active
minutes, 80% meeting the rubric after one revision, and median 4/5 on both
engagement questions. The facilitator schedule allocates 265 active minutes;
that allocation remains unmeasured. Record intervention points and distinguish
self-review from facilitator assessment. The optional live socket activity
also remains outside this read-only rehearsal.
