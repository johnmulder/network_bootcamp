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

Planned commands are `course session create`, `status`, `act`, and `export`,
plus `course learn` and read-only `course doctor`. Existing browsing and practice
commands will remain available. No web service or additional package is needed.
