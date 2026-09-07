# Implementation Validation

The local delivery implementation is complete. This records the initial
technical checks on September 5, 2026, and the documentation consistency
follow-up on September 7. These are not learner-pilot results or proof that a
class will finish on schedule.

## Checks Performed

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
