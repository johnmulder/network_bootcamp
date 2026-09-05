# Implementation Validation

The repository implementation is complete. This records technical checks,
not learner-pilot results or proof that a class will finish on schedule.

## Checks Performed

- All 36 standard-library project tests passed. They cover existing commands,
  default challenge navigation, both capstone forwarding changes, deterministic
  staged evidence, convergence timing, and core/extended setup behavior.
- `./course verify` passed: 36 manifest-tracked evidence files, 83 workbench
  questions across the three modules, and the 17-event original timeline.
- `./prerequisites/setup.sh --check` passed on the development Mac. Core
  readiness uses available commands without refreshing Homebrew metadata.
- All 26 unique read-only evidence commands in the student challenge and
  extension documents ran successfully and produced output. Packet fields,
  the MTU calculation, staged records, and capstone conclusions were reviewed
  against that output and the case conditions.
- A terminal walkthrough reached the one-day introduction and first challenge
  with default selections, preselected Challenge 2 afterward, and returned to
  the main menu and quit successfully. Reference navigation is also tested.
- The agenda and student schedule both total 360 teaching minutes, plus 60
  minutes for lunch and breaks. The facilitator schedule allocates 265 active
  minutes; that allocation has not been measured with students.
- Local document links and anchors, Markdown formatting, and Git whitespace
  checks passed. Student evidence views separate prediction from failure
  outcomes, and solutions are linked for review after an attempt.

## Reproduce the Main Checks

Run from the repository root:

```sh
./prerequisites/setup.sh --check
./course verify
python3 -B -m unittest discover -s tests -v
markdownlint-cli2 "**/*.md"
git diff --check
```

Markdown lint is a maintainer tool, not a student prerequisite. Optional
Zeek/iperf3 exercises use `setup.sh --extended`; they are outside core readiness.

## Learner Validation Still Needed

No real beginner, experienced-learner, or solo learner pilot was run during
implementation. No engagement scores, class completion times, or learning gains
are claimed. Use the [pilot worksheet](pilot.md) with actual learners to assess
those outcomes and adjust the course. The optional live socket activity was
not part of the read-only evidence-command walkthrough.
