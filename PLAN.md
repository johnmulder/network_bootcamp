# Plan: Automating Bootcamp Delivery

Status: proposed implementation; no delivery changes made yet.

## Recommendation and Scope

Add a local course runner around the existing Markdown, fixtures, and Python
workbenches. It should guide a learner through one decision at a time, preserve
their work, provide feedback, and expose the same operations to a script.
The current project already supplies most of the teaching content and evidence.
The missing part is a reliable way to deliver and record the learning sequence.

Assume the first target is independent study on the supported Mac, with an
optional facilitator reviewing local exports. Preserve the six teaching hours,
60 minutes of breaks, six challenges, opening diagnostic, and individual exit.
Installation remains outside teaching time. A scriptable interface also lets a
future website, cohort tool, or assistant deliver the same course without
parsing terminal output or duplicating its rules.

Use Python's standard library and the existing tools. Start with one course
definition and one delivery module. A hosted service, accounts, database, LMS
integration, AI grading, browser interface, and cross-platform installer are
outside this first implementation. Reconsider them after the local runner has
been used successfully. Automatic delivery must preserve prediction, evidence
inspection, revision, and technical explanation as learner activities.

## What Exists and What Must Change

Review baseline: commit `468b971`. During this review, `./course verify` passed
for 36 fixture files, 83 questions, and the 17-event incident timeline.
`./course --help` confirms the current command surface below. The existing
[validation record](facilitator/validation.md) documents the earlier test run;
an actual learner pilot is still outstanding.

| Area | Current implementation | Required addition or modification |
| --- | --- | --- |
| Navigation | [course.py](course.py) prints or pages a whole challenge and preselects the next number. | Add an explicit sequence of phases, next actions, and completion conditions. Viewing a document must not mark it complete. |
| Course definition | Order comes from filenames; timing, prerequisites, and reveal rules live in prose. | Add stable block, phase, checkpoint, and evidence IDs with validated references to existing content. |
| Evidence | The [fixture builder](labs/build_fixtures.py) produces deterministic, manifest-checked local data, including three incident rounds and two independent capstones. | Reuse it; attach provenance and evidence versions to sessions and results. |
| Reveals | [Challenge 4](challenges/04-resilience-budget.md) and [Challenge 5](challenges/05-suspicious-is-not-proven.md) rely on students stopping before later commands and text. | Serve only the current phase; record a prediction or explicit skip before releasing the next view. |
| Workbenches | All three scripts mix question logic with `input()` and printing. Questions have no stable IDs; a completed run exits zero regardless of score. | Separate evaluation from terminal interaction and return structured learning results. Preserve current CLI behavior. |
| Learner work | Templates are copied manually into `work/bootcamp`; the CLI saves nothing. There is no repository `.gitignore`, and `work/` is not currently ignored. | Create isolated session directories, preserve edits, add save/resume, and ignore learner output in Git. |
| Assessment | [Rubric](facilitator/README.md#assessment) scores mechanism, evidence, uncertainty, and action; quizzes are optional practice. | Automatically check objective facts and artifact structure; record self or facilitator review separately for reasoning. |
| Setup | [setup.sh](prerequisites/setup.sh) checks command presence, requires Homebrew even in check mode, and regenerates fixtures in install mode. | Separate capability checks, installation, and explicit fixture rebuilding; report actionable readiness results. |
| Delivery validation | [tests/test_project.py](tests/test_project.py) covers existing code, but there is no saved course journey or checked-in CI workflow. | Add end-to-end delivery tests, content-contract checks, and a repeatable automated verification job. |
| Feedback | [pilot.md](facilitator/pilot.md) is filled in by a facilitator. | Collect local progress and optional learner feedback, and export a review summary using the same rubric and pilot fields. |

## Teaching Behavior to Preserve

The runner should make it easier to investigate, without doing the investigation
for the learner. Show the purpose of each evidence command before offering to
run it. Ask for a prediction, let the learner inspect the output, then ask for
an explanation. Keep commands visible and copyable so tool use remains part of
the course. Allow free text and existing Markdown/CSV artifacts.

Give hints on request without a score penalty. A wrong factual answer should
point back to a relevant field and allow revision. Show worked explanations
after an attempt or an explicit reveal request, and distinguish revealed work
from an independent answer. Suggest a targeted reference or optional practice
set when useful; do not insert a mandatory detour that extends the day.

Keep the following concepts explicit in checkpoints and review prompts:

- Local versus routed delivery, MAC versus IP destinations, DHCP/DNS roles,
  longest-prefix matching, and the return path.
- TCP handshake versus application success, MTU/MSS and header arithmetic,
  retransmission, and the limits of a capture point.
- Control-plane changes versus installed forwarding and observed recovery;
  BGP policy choices and separate VRF lookup contexts.
- Stateful failover, routing symmetry, NAT, WAN health, shared failure domains,
  cloud return routes, and policy intent versus actual enforcement.
- Timestamp normalization, derived versus independent evidence, process and
  socket attribution gaps, proportionate action, validation, and rollback.

Provide solo instructions by default and the existing role swaps for pairs.
For paired study, use one session per learner, optionally sharing an anonymous
pair label. Each learner records their own prediction and exit answer; shared
artifact references must not turn a group result into individual attainment.

## Delivery Design

### 1. A Small, Explicit Course Definition

Add `delivery/course.json` with a versioned, fixed schema. It describes this
course; it does not need a general branching or plugin system. Include:

- Course version and eight required blocks: opening, six challenges, exit.
- Stable phase IDs such as `c02.predict` and `c05.round2`, independent of titles
  and directory positions.
- Ordered phases, prerequisite phase IDs, suggested minutes, and break cues.
- Content references, permitted evidence-view IDs, hint references, checkpoint
  IDs, artifact targets, and the completion requirement for each phase.
- Explicit team/exit case assignment, defaulting to A/B, with a supported B/A
  alternative chosen at session creation.

Keep instructional prose in its existing Markdown files. Add unique start/end
comment markers around delivery fragments and reference those fragment IDs
from the definition. Markers allow a fragment to contain a heading, table, and
command without maintaining a second copy. Split combined sections at actual
decision points, particularly Challenge 4's choices, outcomes, and power twist.
Add equivalent fragments to hints and worked solutions.

Validation must reject duplicate or missing IDs, missing or overlapping
fragments, nonexistent evidence/checkpoints, invalid dependencies, and cycles.
Check that the eight blocks total 360 teaching minutes and breaks total 60;
count the exit block once even though its prose lives in Challenge 6. Keep
[agenda.md](agenda.md) as the curriculum authority and check its schedule
against the definition. Do not convert all 104 reference guides into phases.

The guided view should omit later fragments, solution links, diagnostic
filenames, and full-timeline shortcuts until their intended review point.
Direct document and fixture access remains available. This is a learning
sequence, not an exam-security or access-control system.

### 2. Durable Sessions and One Shared Execution Path

Add `delivery.py` for definition validation, phase transitions, session storage,
and checkpoint dispatch. Extend `course.py` as its CLI adapter. Both terminal
and headless delivery must use these same functions.

Create `work/<session-id>/` containing one `session.json` and the existing three
Markdown templates plus ledger CSV. Add `/work/` to a new `.gitignore`.
Use a restricted session-ID format and paths confined to the session directory;
reject traversal and symlinks that escape it. Never overwrite an existing
session or learner-edited artifact during creation, resume, or export.

Store the schema/course versions, a digest of delivery content and evaluation
code, fixture-manifest digest, case assignment, practice seed and selected
question IDs, current phase, submissions, revisions, hint/reveal use, artifact
references, and review results. Record timestamps and learner-supplied timing
separately. File presence or elapsed wall time does not demonstrate learning.

Use atomic replacement for the JSON state and a short single-writer lock.
Mutations carry an expected revision and request ID so stale clients fail
clearly and retrying a request cannot advance twice. Preserve the original
prediction when a learner revises it. Save accepted responses before advancing;
quitting, EOF, or interruption must leave a resumable phase.

Check saved versions against current course content and verified fixture hashes
on resume. On mismatch or corrupt state, report a recovery path and preserve
the old files. Initially require the matching course version or a new session;
do not silently migrate results or reset progress. Existing `work/bootcamp`
files remain usable through the manual route; provide documented copy/import
steps without inferring prior completion from those files.

### 3. A Headless Contract, Then a Terminal Wrapper

The following commands are proposed interfaces, not commands available today:

| Interface | Purpose |
| --- | --- |
| `./course session create --id practice-01 --mode solo --case A --json` | Validate readiness and initialize a new session with A reserved for the main capstone and B for exit. |
| `./course session status --id practice-01 --json` | Read current phase, prompt, artifact references, review status, and allowed actions without advancing. |
| `./course session act --id practice-01 --input request.json --json` | Submit a typed action: prediction, answer, evidence request, hint/reveal, review, continue, or explicit skip. |
| `./course session export --id practice-01 --format json` | Emit a portable summary; also support Markdown review and CSV progress output. |
| `./course learn --id practice-01` | Present the same sequence interactively and resume from saved state. |

Use a small fixed set of action handlers. An action request includes
`request_id`, `expected_revision`, `phase_id`, action type, and its payload.
Accept long answers through a JSON file or stdin. Return a versioned JSON
envelope with operation status, session revision, current phase, learning
result, feedback, and permitted next actions.

In JSON mode, write exactly one JSON document to stdout, including failures;
send incidental diagnostics to stderr. Never prompt, invoke a pager, or
interleave child-process output with JSON. Exit zero means the request was
processed; incorrect, revealed, skipped, incomplete, and pending-review are
explicit learning states. Use nonzero codes for malformed requests, invalid
transitions/version conflicts, or execution failures and document the mapping.
Callers must not interpret process success as course completion.

Keep existing `day`, `challenge`, `guide`, `practice`, `timeline`, and `verify`
commands compatible. Switch the default terminal menu to the runner only after
all required blocks work. Keep a clearly labeled read-only browsing option.
Do not require terminal scraping, synthetic keystrokes, or a web server.

### 4. Named Evidence Views and Read-Only Readiness

Define named evidence commands in trusted Python code, referenced by ID from
the course definition. Reuse the existing `tshark`, `jq`, and table views.
Execute fixed argument arrays with `shell=False`, a known repository working
directory, timeouts, and captured output. Accept only validated parameters
such as the already-assigned case. Learner text never becomes shell code,
a filter expression, a command name, or an unrestricted path.

Do not execute Markdown code blocks automatically. They remain the manual
instructions and should be checked against the named views for drift. Preserve
fixture paths and frame/record IDs with captured results. Limit output size,
report truncation and tool errors explicitly, and allow an unchanged phase to
retry after a missing-tool or timeout failure.

Session actions may inspect saved evidence; they must not invoke setup,
Homebrew, packet capture, networking changes, or external targets. Reuse the
existing neutral transfer view and staged incident files. Use the established
evidence map to keep derived views and independent cases distinct.

Add `./course doctor --json` for read-only checks of the platform, Python,
required command capabilities, evidence integrity, and delivery definition.
Check representative TShark fields and jq operations rather than relying only
on executable presence. Report versions for diagnosis and separate core,
extended, and optional live-tool readiness. Homebrew is required to install
missing packages, not to inspect an already usable environment.

Modify setup so installation, verification, and fixture rebuilding are explicit
operations. Use the committed fixtures after validating them; a routine learner
setup must not regenerate the evidence behind an existing session. Retain the
builder as an explicit maintainer operation and document how to recover missing
or damaged fixtures. A doctor failure should provide a concrete next command
without running it or silently falling back to precomputed answers.

### 5. Objective Feedback and Honest Review Status

Add explicit stable IDs to all 83 workbench questions. Extract answer evaluation
into pure functions that return result data; keep fixture-derived answers and
the current deterministic selection. Do not derive identity from question text
or shuffled position. Store selected IDs as well as the seed when resuming.

Reuse existing route, VRF, cloud, and timeline functions for suitable checks.
Keep internal answer sets and worked explanations out of pre-attempt output.
Do not turn the existing demo path's `correct=True` into a learner score.
Represent attempts, hints, answer reveals, correctness, and revisions explicitly.

| Block | Suitable automatic check | Explanation still requiring review |
| --- | --- | --- |
| Opening | Local-subnet decision and structured responses to the diagnostic. | What the handshake changes about the learner's hypothesis. |
| Packet | Winning prefix/eligible next hops before and after removing the host route. | MAC/IP roles, observed versus modeled headers, and return-path limits. |
| Transfer | Payload calculation of 1160 bytes under the stated headers, with units. | Why an ICMP observation does not prove endpoint receipt or handling. |
| Link | Recorded 80 ms interval, surviving next hop, BGP choice, and VRF lookup. | Why the interval does not measure successful application recovery. |
| Resilience | Two valid token choices, route lookups, and required flow rows. | Tradeoffs, stateful failure, shared dependencies, and residual risk. |
| Incident | UTC normalization, valid evidence references, and ten-field CSV structure. | Claim quality, attribution gaps, independence, scope, and proportionate action. |
| Handoff/exit | Assigned case ID, changed route/context, and valid observation IDs. | Integrated mechanism, uncertainty, owned next step, and individual explanation. |

Artifact checks can report missing fields, invalid references, or the narrative
length limit. They cannot establish that a claim is supported. Keep the three
editable deliverable bundles as the authoritative long-form work; store short
checkpoint answers and artifact references in session state. Snapshot artifact
hashes when reviewed, and mark the review stale if later edits change them.

Record each rubric dimension from 0–2, feedback, reviewer type (`self` or
`facilitator`), and pre/post-revision scores. Preserve the current 6/8 minimum
with no zero and the individual exit explanation. Report delivery finished,
objective checks satisfied, self-reviewed completion, and facilitator-reviewed
completion separately. A skipped phase, demonstrated answer, or pending review
must not be labeled an independent pass. Offer explicit skips with reasons so
learners can continue without hiding unfinished work.

### 6. Pacing, Exports, and Facilitator Support

Show suggested phase durations and upcoming break cues. Advance on an explicit
learner action, never merely because a timer expired. Learners can quit and
resume across days. Avoid enforcing a six-hour countdown or revealing the next
incident round while someone is still explaining the previous one.

Export phase status, factual checks, hints/reveals, skipped work, assigned cases,
rubric reviews, artifact references, and the existing two engagement ratings.
Keep timestamps, self-reported durations, and observed active learning minutes
distinct; the CLI cannot infer active thought from process uptime.

Use anonymous session labels and local storage. Default progress summaries omit
free-text answers and names. Include learner artifacts only through an explicit
export choice and name the included files. Export is local and portable; it
does not upload, email, or submit work anywhere. Document how a facilitator can
review an exported bundle and record feedback against its version and hashes.
This first version needs no central roster, live dashboard, or automatic mail.

## Implementation Sequence and Commit Boundaries

Each numbered change should be independently reviewable, with a one-line commit
message after its checks pass. Implement only the first slice before expanding
its schema or adding more infrastructure.

1. **Define the delivery contract and isolate Challenge 2.** Add
   `delivery/course.json`, its validator, initial content fragments, and
   `delivery/README.md` documenting the proposed interfaces and state meanings.
   Inventory all required phases, but flag unfinished handlers explicitly.
   Add a small `tests/test_delivery.py` covering fragment references, IDs, and
   schedule arithmetic. Keep the current course entry point unchanged.
   Suggested commit: `Define course delivery phases and contracts`.
2. **Deliver one resumable challenge end to end.** Add `delivery.py`, session
   creation/storage, headless status/action commands, `.gitignore`, read-only
   doctor, and the necessary setup separation. Implement Challenge 2's
   prediction, named packet views, calculation, hints, and review state. Verify
   a wrong answer, correction, interruption, restart, and export with a script
   using no terminal input. Suggested commit:
   `Add resumable automated delivery for the transfer challenge`.
3. **Expose reusable workbench results.** Modify all three workbench scripts
   and their existing tests to add stable question IDs and pure evaluation.
   Connect the selected objective checks to the session runner. Preserve all
   current practice commands and answers, including demonstration semantics.
   Suggested commit: `Expose structured workbench questions and results`.
4. **Wire the full day and terminal experience.** Expand fragments and handlers
   across opening, Challenges 1–6, hints, solutions, and exit. Preserve both
   A/B assignments, incident round decisions, the budget reveal, role prompts,
   and breaks. Add `learn`, workspace-aware instructions, and current-phase
   artifact links. Update README, agenda, prerequisites, and facilitator docs;
   make the runner the default only now. Suggested commit:
   `Deliver the full bootcamp through staged guided sessions`.
5. **Complete review and local reporting.** Add artifact validation, review
   snapshots, revisions, separate completion states, export formats, and
   feedback collection. Align facilitator/pilot instructions and examples with
   those exports. Suggested commit:
   `Add artifact review and portable course results`.
6. **Automate verification and rehearse delivery.** Finish failure-path and
   whole-course tests, add a CI workflow, and update the validation record with
   reproducible commands and limitations. Build and test a distributable archive
   from tracked course files, excluding learner work. No external publishing is
   part of this change. Suggested commit:
   `Verify automated delivery and document the release workflow`.

## Acceptance Checks

### Automated Implementation Checks

- Run all existing tests and `./course verify`; extend verification to validate
  the delivery definition, fragments, checkpoint IDs, and evidence references.
- Run a headless journey through all eight blocks on temporary session storage.
  Include an incorrect attempt, hint, reveal, revision, skip, and resumed phase.
  Confirm that all required independent work and reviews are needed for their
  corresponding completion claims.
- Test A/B and B/A assignments, reserved exit isolation in guided output, the
  three incident rounds, and the budget choice/outcome/twist sequence. A status
  read or repeated request must not reveal or advance a later phase.
- Test duplicate requests, stale revisions, concurrent writes, interrupted
  persistence, corrupt state, missing artifacts, changed artifact hashes, and
  course/fixture version mismatches. Existing learner data must survive failures.
- Exercise malformed JSON, unknown IDs, invalid transitions, invalid units,
  missing tools, nonzero tool exits, output truncation, and command timeouts.
  Verify that machine output remains valid JSON on success and failure.
- Reject paths escaping the workspace, shell expressions in action payloads,
  and evidence requests not permitted in the current phase. Hash the fixture
  tree before and after a journey to confirm delivery never modifies it.
- Validate the three templates and ten-field ledger, meaningful factual
  answers, and rubric thresholds. Do not test prose by requiring an exact
  preferred narrative or architecture recommendation.
- Check new/changed Markdown, local links, and whitespace. Add a CI job for
  standard-library tests and content checks with fake tools. Add a Mac smoke
  job using real core tools to exercise every registered evidence view and
  required packet field. Dependency installation occurs during CI provisioning;
  course execution itself requires no network.
- Create a clean course archive including checked-in fixtures, content, and
  version metadata. Extract it at a path containing spaces and run doctor,
  verification, and the headless journey without Git metadata. Confirm exports
  remain understandable when moved and that the archive excludes `work/`.

### Human Delivery Checks

Observe at least one beginner working solo without a facilitator choosing the
next command or reveal. Also rehearse paired delivery with separate individual
exit answers. Use the existing pilot worksheet plus exported results to record
where explanations, tool output, or navigation require intervention.

Retain the existing targets: first observation within 15 minutes, six teaching
hours, at least 210 active minutes, 80% meeting the rubric after one revision,
and median 4/5 on both engagement questions. These are validation targets, not
outcomes that automation can guarantee. Distinguish student results from
scripted test results and self-review from facilitator assessment.

The implementation is complete when the automated checks pass, all required
blocks work in terminal and headless modes, documentation matches the behavior,
and remaining human validation is explicitly recorded. Claim that independent
delivery works with students only after the human pilot; use its findings to
decide whether a browser interface or cohort integration is worth adding.
