# Course Delivery Contract

The runner delivers all 36 phases across eight teaching blocks. Start or resume
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
Optional saved practice appears at the Module 1, 2, and 3 review phases, after
the relevant evidence has been released. It never changes the course grade.

Reusing an identical request ID returns its original result. A reused ID with
different input or a stale revision fails. Exit codes are 0 for a processed
request (including an incorrect answer), 2 for invalid input, 3 for a session
or transition conflict, and 4 for execution/readiness errors. JSON errors remain
on stdout; diagnostics for non-JSON requests use stderr.

Setup now checks committed evidence rather than rebuilding it. To deliberately
regenerate evidence as a maintainer, run `python3 labs/build_fixtures.py`; existing
sessions require their matching evidence version. Never rebuild as an automatic
session recovery step. No web service or additional Python package is needed.
