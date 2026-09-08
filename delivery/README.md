# Course Delivery Contract

The runner delivers all required phases across eight teaching blocks. Start or resume
with `./course learn --id my-session`, or use the JSON session commands below.
The default `./course` menu opens saved delivery; manual browsing is also kept.

`course.json` gives phases stable IDs and ordered prerequisites. Teaching prose
stays in Markdown between matching `delivery:start` and `delivery:end` comments.
The validator checks references and the 360-minute teaching / 60-minute break
schedule against the agenda. It rejects overlapping fragments and dependencies
that violate the linear course order.

The runner uses a local `work/<id>/session.json`, atomic writes, request IDs,
and revision checks. Terminal and JSON commands call the same delivery
functions. JSON operation success is separate from learning results:
incorrect, revealed, skipped, incomplete, or pending review is not a pass.

Use `./course session create --id example --json`,
`status --id example --json`, `act --id example --input request.json --json`,
and `export --id example --format json`. All operations follow `./course session`.
All challenges, opening, and exit use staged prompts and factual checkpoints.
`./course doctor --json` performs read-only readiness checks without printing
the inspected evidence. Terminal delivery follows the same headless interface.

An action request has `request_id`, `expected_revision`, `phase_id`, `action`,
and a `payload` object. Get the current prompt and permitted actions with status.
For prediction/reflection, submit `text`; for checkpoints, also submit `answers`
keyed by the checkpoint IDs. `continue` advances after an answer; `skip` requires
a reason. Evidence requests use `view`; hints and reveals use an empty payload.
The `--input -` option reads a JSON request from stdin without prompting.

Use `status --phase c02.calculate` to revisit a released phase for correction;
status reads never advance. In the terminal, g selects a released phase. q or
Ctrl-C exits after preserving accepted responses. Edit the artifact paths shown
in each phase before recording a rubric review. Breaks and suggested minutes
are advisory, and an optional duration on `continue` is self-reported time.

Case A is the main capstone and B the exit unless `--case B` was selected when
creating the session. That assignment is saved. `--mode pair --pair-label team-1`
adds pair instructions; each learner still needs their own session and exit.
Support and fresh reassessment are available in conceptual checkpoint phases.
Recommendations follow recorded mistakes. The fixed random-five saved practice
is replaced; standalone workbench menus remain available for optional study.

Reusing an identical request ID returns its original result. A reused ID with
different input or a stale revision fails. Exit codes are 0 for a processed
request (including an incorrect answer), 2 for invalid input, 3 for a session
or transition conflict, and 4 for execution/readiness errors. JSON errors remain
on stdout; diagnostics for non-JSON requests use stderr.

Setup now checks committed evidence rather than rebuilding it. To deliberately
regenerate evidence as a maintainer, run `python3 labs/build_fixtures.py`; existing
sessions require their matching evidence version. Never rebuild as an automatic
session recovery step. No web service or additional Python package is needed.

## Start a Session

Run from the repository root after installing prerequisites:

```sh
./course doctor --json
./course session create --id example --mode solo --case A --json
./course session status --id example --json
```

Creation copies the three templates and ledger once. IDs contain lowercase
letters, digits, and hyphens, with a 48-character limit. An existing directory
is never overwritten. For paired study, add `--mode pair --pair-label team-1`;
give each learner a different session ID. Mode and case options apply only when
creating a session; resuming uses its stored assignment.

The first phase is `opening.predict`. Save a request such as this under
`work/example/request.json`, then submit it:

```json
{
  "request_id": "opening-first-attempt",
  "expected_revision": 0,
  "phase_id": "opening.predict",
  "action": "predict",
  "payload": {
    "text": "My first hypothesis is a size-dependent failure. I would request packet sizes and feedback because the connection can start."
  }
}
```

```sh
./course session act --id example --input work/example/request.json --json
```

Use the returned revision for your next request, a new request ID for each
new action, and `continue` with an empty payload to advance. Keep the original
request ID and body when retrying after a lost response. Retries return the
original response, so fetch status afterward if other actions may have occurred.
Status and export do not change the session revision.

## Action Payloads

The status response supplies only the current/revisited phase's prompt,
checkpoint IDs, permitted evidence views, and allowed actions. Every action
requires the same five envelope fields shown above.

| Action | Payload | Effect |
| --- | --- | --- |
| `predict` / `answer` | `text`; checkpoint phases also need `answers` mapping every displayed ID to a short string | Saves a new attempt and factual feedback without advancing. Keep long-form work in the artifact files. |
| `evidence` | `view` copied from the phase's evidence list | Runs a fixed read-only command and returns captured output, command, and fixture-manifest hash. |
| `hint` | `{}` | Reveals answer-bearing help and marks unfinished attempts in this block supported. |
| `reveal` | `{}` | Shows only this block's worked review and assigned case. Subsequent answers exposed by it cannot count as independent. |
| `continue` | `{}` or optional numeric `minutes` | Advances after required responses; review can remain pending. Minutes are self-reported. |
| `skip` | Nonempty `reason` | Continues while recording unfinished work. Revisit and finish it later to satisfy completion. |
| `review` | `reviewer`, `scores`, `feedback`, `expected_artifact_hashes`, `expected_response_sha256` | Records a self/facilitator rubric review of specific file and response versions. |
| `feedback` | Optional integer `wanted_to_know` and `manageable` ratings, 1–5; optional `text` | Records the existing engagement questions. An empty object opts out. |

Checkpoint answers retain the existing workbench normalization and aliases.
Units matter where requested. For `budget.options`, supply exactly two of
`state-sync`, `backup-path`, `monitoring`, and `management`, separated by commas.
No choice receives an automatic architecture-quality score.

The JSON interface never invokes a pager or asks for input beyond the supplied
request file/stdin. Unknown actions, unreleased evidence, stale revisions, and
invalid paths fail without changing state. Evidence failures preserve the phase
for retry. It never runs shell text from an answer or Markdown code block.

## Artifacts and Review

Retain the template section headings, fill empty table cells and placeholders,
and preserve the narrative/handoff markers. Put the exact capstone ID in the
existing case-ID fields, not in renamed section headings. Write unknown with a
reason when evidence is absent. The incident narrative and written handoff have a
150-word limit. Diagrams can be expressed as text and tables in the Markdown.

The ledger retains its ten fields. Use an original filename such as
`incident/firewall.jsonl` as `source`, and `incident/firewall.jsonl#1` as
`evidence_id`. The suffix is a one-based record number. Keep the raw timestamp
verbatim and express the same instant in UTC in `normalized_time`. Select six
to eight original incident records. Append assigned capstone rows separately,
using their supplied observation IDs and exact case filename as the source.
Fill all ten cells; collection coverage can be unknown.

At a review phase, status returns structural errors and current artifact hashes.
It checks required sections, placeholders, CSV shape, source references, and
timestamps. These checks do not assess narrative truth, architecture merit,
or whether a proposed action is proportionate.

For `review`, `reviewer` is `self` or `facilitator`; `scores` maps `mechanism`,
`evidence`, `uncertainty`, and `action` to integers 0–2. Supply nonempty feedback
and copy the status response's `artifact_hashes` to `expected_artifact_hashes`.
Also copy its `response_sha256` to `expected_response_sha256` so a review cannot
silently assess responses changed after the reviewer read them.
Scores are retained even when work needs revision. A valid rubric review needs
at least 6/8, no zero, and structurally complete artifacts. Reviewer type is a
local label, not authenticated identity or certification.

Reviews snapshot the files and the block's submitted responses. Editing a file
or revising those responses makes affected reviews stale. File hashes cover the
whole artifact, so refresh relevant reviews after final capstone/exit edits.
Use g in the terminal, or `status --phase c01.review` and a new review action.
A facilitator using an exported bundle must use that bundle's artifact hashes;
feedback for an older file version is rejected instead of applied to new work.

The [course completion policy](../agenda.md#completion-and-feedback) applies to
both manual and guided delivery. The JSON response reports:

| Field | Requirement |
| --- | --- |
| `delivery_finished` | Reached the end of all implemented phases; skips or demonstrations can remain. |
| `required_work_recorded` | All phases are complete, demonstrated, or pending rubric review, with valid artifact structure; no skipped or incomplete phases remain. |
| `objective_checks_satisfied` | Every conceptual objective has an independent first response or fresh reassessment; recording checks are part of required work. |
| `self_reviewed_completion` | All three conditions above and passing, current self-reviews for Challenges 1–6 and the exit. |
| `facilitator_reviewed_completion` | All three conditions above and passing, current facilitator reviews at those same seven points. |

The first committed response qualifies only if correct before corrective
feedback or answer-bearing help. Corrections remain supported; invalid factual
formats do not consume an attempt. A fresh, unassisted reassessment can satisfy
the same objective without rewriting the original history. Assignment is saved
before presentation, resumes unchanged, and cannot be rerolled by retrying a
request. A hint on a fresh variant exposes it permanently. Exhaustion explicitly
leaves the objective unmet. See the [learning action contract](assessment.md#typed-learning-actions).
The status and JSON export include per-objective original and fresh attainment;
summary exports omit responses, prose, and authored answer keys.

State and protocol version 2 reject old sessions without migration or regrading.
Use their matching course copy to resume or export them; create a new session
for the new course. Standalone workbench quizzes remain optional practice.

Before capstone and exit diagnostic material, use `diagnose` with two
`hypotheses`, `confidence` (`low`, `medium`, `high`), and `next_evidence`
(`state`, `observations`, `conditions`). Status initially exposes only the
symptom and flow. After recording that diagnosis, choose those evidence views
in any order; update your explanation as evidence changes your claims. The
local files remain readable by convention, not a secure exam boundary.

## Local Exports

### Bounded Experiments

Status exposes an `experiment` model, its finite parameter choices, and saved
attempts in the route, transfer, and resilience activities. Use
`experiment_predict` with `parameters` and a written `prediction`. Then use
`experiment_result` with the returned `experiment_id`. The terminal uses `x`
and `z`. A prediction is saved before any result is returned, and an unfinished
experiment must be compared before starting another. Results retain parameters,
variant ID, model version, and hashes of the unchanged baseline source files.

The required comparisons are in `c01.change`, `c02.calculate`, `c04.outcomes`,
and `c04.twist`; explicit skips remain unfinished work. Resilience uses the
recorded two-token choice before the twist, then permits a revised pair. The
twist is unavailable before its phase. These comparisons occupy the existing
practice minutes. Complete the original factual attempt first when seeking
independent evidence: seeing a model result is answer-bearing help.

Transfer computes a byte bound and whether the selected payload fits. Routing
reuses the workbench's prefix, preference, metric, and VRF selection. Resilience
reports dependencies addressed and residual risks; it does not promise that
state synchronization, failover, or monitoring meets the requirement. These
are computed teaching results, not new captures or evidence of real recovery.
The fixed parameter schemas accept no commands, filters, paths, or live targets.
Default exports include model results and omit written predictions.

### Export Commands

```sh
./course session export --id example --format json
./course session export --id example --format csv --output progress.csv
./course session export --id example --format markdown --include-artifacts --output review.md
```

Default summaries include versions, anonymous labels, assignments, progress,
factual results, rubric score history, hint/reveal use, and optional ratings.
They omit learner answers and review comments. JSON and Markdown accept
`--include-artifacts` to include all four learner files plus response/review
history; the export lists those files. Extra attachments are not bundled.
CSV is a progress table and does not support including free-text artifacts.

Output goes to stdout unless `--output` names a new file under
`work/<id>/exports/`. Output paths cannot escape that directory or overwrite a
file. Exports contain relative source/file references and version hashes, so
they can be reviewed on another machine. Nothing is automatically submitted,
uploaded, or sent to a facilitator.

The JSON export includes the session revision, artifact hashes, and each review
phase's `response_hashes` entry. A reviewer can return a `review` action using
those hashes and a fresh session revision after checking that the course and
response versions still match. Preserve
first and revised scores when recording pilot observations. Timestamps and
self-reported minutes are separate from observed active student minutes.

## Recovery and Maintenance

Accepted actions are atomically saved to `session.json`; a short file lock
prevents simultaneous writers. An interrupted request can be retried with its
original ID. A corrupt state file, unsupported version, or changed evidence
produces a recovery message and preserves existing data. Keep a backup copy of
the session directory. Exports are review records, not a substitute for a full
session backup when resuming on another machine.

Course content and evaluation code are fingerprinted without requiring Git.
Resume using the matching course copy; otherwise create a new session. There
is no automatic migration that mixes versions. History is limited to 32 MiB
per session, requests to 128 KiB, and each artifact to 2 MiB. Named evidence
commands have time and output limits. Hitting a limit preserves prior work.

If an older manual `work/bootcamp` directory already exists, start a different
session ID. Copy your Markdown/CSV files into that new workspace deliberately,
retain its `session.json`, and adapt headings/ledger references to the templates.
Copying files does not infer completion of past phases. Keep the old workspace
until you have checked the copy.

The definition describes this course's linear sequence; `delivery.py` contains
its fixed evidence commands and checkpoints. Validate content markers, question
IDs, and timing with `./course verify`, and run the project tests after edits.
Keep Markdown commands consistent with their registered argument arrays. The
104 reference guides continue to use manual navigation and optional exercises.

## Verify and Package Delivery

Run these checks on a development Mac with core tools installed:

```sh
python3 -B -m unittest discover -s tests -v
python3 -B verification/check_delivery.py
python3 -B verification/check_delivery.py --smoke --journey
```

The content check validates local links/anchors and matches each teaching
command to its registered argument array. The smoke check executes all 25
read-only views. The journey check uses fresh CLI processes, real evidence,
both case assignments, an incorrect answer, save/resume, retry, skipped-work
revision, hints, a reveal, synthetic rubric reviews, and portable exports. Its
temporary session directories are cleaned afterward. These are scripted
technical checks; their scores and timings are not learner-pilot results.

To build a distributable archive, commit or stage the intended source files
first. Packaging reads tracked files from the current checkout, includes the
saved evidence and `RELEASE.json` with content/fixture fingerprints, and excludes
`work/`, Git metadata, and implementation plans:

```sh
python3 -B verification/package_course.py --output work/course.tar.gz --journey
```

Choose a new output filename for later builds; packaging never overwrites one.
The check extracts into a path containing spaces and exercises the course without
Git metadata. `--check` runs the portable checks without requiring the real Mac
tools; `--journey` also runs doctor, evidence smoke, and both full journeys.
The archive preserves executable permissions. Recipients extract it and run
`./prerequisites/setup.sh` before starting their own sessions.

The [CI workflow](../.github/workflows/check.yml) runs the standard-library suite
on Python 3.10 and real delivery on a Mac with Python 3.13. Tool installation
occurs before offline course execution. Its GitHub-maintained
[checkout](https://github.com/actions/checkout) and
[Python setup](https://github.com/actions/setup-python) actions provision the
job; the course itself has no new Python dependencies. The workflow checks an
archive but does not publish a release or upload learner results.
