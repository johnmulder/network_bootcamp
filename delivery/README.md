# Course Delivery Contract

Implementation is in progress. The current menu still opens the manual course.
The definition inventories all eight teaching blocks; `implemented: false`
identifies phases that the new runner cannot deliver yet.

`course.json` gives phases stable IDs and ordered prerequisites. Teaching prose
stays in Markdown between matching `delivery:start` and `delivery:end` comments.
The validator checks references and the 360-minute teaching / 60-minute break
schedule against the agenda. It rejects overlapping fragments and dependencies
that violate the linear course order.

The new runner will use a local `work/<id>/session.json`, atomic writes, request
IDs, and revision checks. Terminal and JSON commands will call the same delivery
functions. JSON operation success will be separate from learning results:
incorrect, revealed, skipped, incomplete, or pending review is not a pass.

The first slice supports `./course session create --id example --json`,
`status --id example --json`, `act --id example --input request.json --json`,
and `export --id example --format json`. All operations follow `./course session`.
Only Challenge 2 is currently delivered; full-course completion remains false.
`./course doctor --json` performs read-only readiness checks without printing
the inspected evidence. Terminal delivery will follow the headless interface.

An action request has `request_id`, `expected_revision`, `phase_id`, `action`,
and a `payload` object. Get the current prompt and permitted actions with status.
For prediction/reflection, submit `text`; for checkpoints, also submit `answers`
keyed by the checkpoint IDs. `continue` advances after an answer; `skip` requires
a reason. Evidence requests use `view`; hints and reveals use an empty payload.
The `--input -` option reads a JSON request from stdin without prompting.

Reusing an identical request ID returns its original result. A reused ID with
different input or a stale revision fails. Exit codes are 0 for a processed
request (including an incorrect answer), 2 for invalid input, 3 for a session
or transition conflict, and 4 for execution/readiness errors. JSON errors remain
on stdout; diagnostics for non-JSON requests use stderr.

Setup now checks committed evidence rather than rebuilding it. To deliberately
regenerate evidence as a maintainer, run `python3 labs/build_fixtures.py`; existing
sessions require their matching evidence version. Never rebuild as an automatic
session recovery step. No web service or additional Python package is needed.
