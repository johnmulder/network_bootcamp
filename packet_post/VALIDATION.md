# Packet Post Validation Record

## Release Status

Software preview, September 17, 2026. Eight missions contain 27 authored
decisions. The requested software implementation is complete; observed
learner trials and independent human review remain pending by the project
owner's explicit decision. No learning-effectiveness claim, curriculum
replacement, or independent attainment follows from these technical checks.
The original implementation plan was retired; this record retains the pending
human work and the technical release evidence.

## Student Readiness Gates

September 18, 2026: the student-readiness plan is being executed. This is
still a software preview. No student trial, independent human review,
or direct second-device/accessibility observation has been recorded.
Preparation and automated checks do not satisfy those human gates.

The project owner states that student trials and independent networking
review will take place this weekend (September 19-20). Those results remain
pending. The owner directs that the second-Mac test be assumed complete;
that acceptance is recorded as an owner assumption, not a test we observed.
No second-device configuration, tester identity, or checklist was supplied.

| Gate | Status | Evidence and remaining work |
| --- | --- | --- |
| G0: Trial prepared | Pending | Start card, runbook, staff items, worksheets, and frozen candidate inventory prepared; actual participants, prerequisites, and named facilitators/reviewers to be recorded at the weekend trial |
| G1: Operable and recoverable | Passed | Owner accepts the second-Mac test by assumption; local save/layout/startup regression checks passed. Physical input and accommodation observations were not supplied and are not claimed as directly verified |
| G2: Technically sound | Pending | Owner schedules independent networking review for September 19-20; decision and trial-item approval awaited |
| G3: Usable with students | Pending | Owner schedules student trials for September 19-20; no participant observations received |
| G4: Supports intended reasoning | Pending | No human-rated unseen transfer responses recorded |
| G5: Classroom release prepared | Pending | Offline preview bundle and synthetic support/recovery rehearsal passed; human gate results, candidate-specific remote CI, and final release decision remain open |

Facilitator, independent networking reviewer, second-Mac tester, and
participant names: **not supplied**; the owner has supplied the weekend
schedule and second-Mac acceptance. Target environment for the first
trial remains a provisioned Apple Silicon Mac with Python 3.13. Qualified
student-facing mission set: **none yet**; all eight retain preview status.

The [student start card](README.md#student-start-card) and
[facilitator runbook](README.md#facilitator-runbook) are available. They
include prerequisites, course review gates, individual save IDs, error
recovery, and the existing course as an accommodation route that must itself
be checked with the student who needs it.

Use the [prepared observation worksheet](../facilitator/packet-post-pilot.md)
for actual sessions. The separate local staff packet under
`work/packet-post-readiness/staff/` contains three new route/VRF items,
two transfer items for each other mission, separate proposed answer keys,
and all 27 authored decisions with empty independent-review fields.
These are prepared materials awaiting review, not student results. Keep
unassigned questions and keys outside the student distribution.

| Mission | Actual observed completions | Rule/limit teach-backs | Participant/version references | Open finding |
| --- | --- | --- | --- | --- |
| Sorting | 0 | Pending | Pending | Awaiting weekend trial |
| Parcel | 0 | Pending | Pending | Awaiting weekend trial |
| Bridge | 0 | Pending | Pending | Awaiting weekend trial |
| Resilience | 0 | Pending | Pending | Awaiting weekend trial |
| Suspicious Crumbs | 0 | Pending | Pending | Require participant's current c05 review |
| Handoff | 0 | Pending | Pending | Awaiting weekend trial |
| Return Receipt | 0 | Pending | Pending | Require participant's current c06 and exit reviews |
| Foundations | 0 | Pending | Pending | Awaiting weekend trial |

The latest observed remote CI run succeeded for earlier commit
`9a97add89774c8e31d8e2f9c1877b0eb200384ea` on September 13. It does not
cover this candidate or qualify the new renderer job. Candidate-specific
remote CI is still pending; local changes have not been pushed.

### Completed Engineering and Weekend Handoff

The frozen software candidate is
`86b7238d82e6972b831150d3cd2f50d801256f90`. Later documentation records these
results without changing its packaged source. Three reproduced defects
were fixed: failed text saves now keep the editor available for retry,
the shared-power decision prompt is fully visible at the minimum grid
size, and importing through a filesystem alias can start a new game.

| Check actually completed on September 18 | Result |
| --- | --- |
| Full repository unittest suite after the final fix | 138 passed in 76.829 seconds |
| Targeted game tests | 14 passed, including failed-save and alias-startup regressions |
| Three-size renderer and actual local desktop window | All eight missions and 27 decisions passed; complete prompts and visible save errors checked; Metal/SDL 3.2.16 used |
| Fresh TShark comparison | Both stored capture projections matched |
| `verification/package_course.py --output work/packet-post-readiness/candidate-v2.tar.gz --journey` | 284 tracked files plus metadata passed all archive checks and both 36-phase real-tool course journeys |
| Fresh environment with supplied exact wheels | Offline install passed with `--no-index --require-hashes`; six transitive/direct packages pinned with SHA256 |
| Extracted-copy synthetic rehearsal | All missions rendered; separate processes resumed and exported a committed prediction; a closed save copied into a matching course copy retained its state and created a third distinct export |
| Final student/staff ZIPs | Payload checksums, archive integrity, relative links, and startup from a path containing spaces verified |
| Trial-material author screening | 17 new question/key pairs, independent route arithmetic, header budgets, UTC conversions, and 27 pending human-review rows checked |
| Documentation | Markdown and local-reference checks passed |

The archived candidate's game fingerprint is
`73aede2b31bfd3e80662449d89f6e150a1b4621deff502f9de6c3f0ecd3b0b60`.
The alias fix changes it from the prior game version. Existing saves must
use their matching copy; the previous source archive remains locally at
`work/packet-post-release.tar.gz`. No state file or fingerprint was migrated
or reset. Core course content and fixture hashes are unchanged.

The following local artifacts are ready for the owner-coordinated weekend
work. They are intentionally outside Git and course source archives. The
student ZIP contains the frozen course/game source, exact wheels, checksum
inventory, installation instructions, and technical check record. It omits
the newly authored pilot questions/keys and all participant data. The staff
ZIP contains those separate questions/keys, blank observations, and review
records. Keep it with the facilitator and expose only assigned questions.

| Local artifact under `work/packet-post-readiness/` | SHA256 |
| --- | --- |
| `packet-post-weekend-preview.zip` | `f9fc0300dcd69acc373d116efa6e7650a6306592d54f8f8de456266b6402a153` |
| `packet-post-weekend-staff.zip` | `28c66f5b55d82834cc7345f0dc70fb1f68f16a8b26f6e79ccb9c70c3ab27e29f` |

Return the reviewer judgments and observed participant outcomes with their
candidate version. Resolve material findings, recheck affected behavior,
and record the exact accepted mission/device scope before classroom
promotion. The readiness plan remains open until these results and the
release decision are recorded; a scheduled trial is not a completed trial.

The game remains optional, outside the required 360-minute course. It never
awards course credit or changes course answers or reviews. Original incident
and recovery practice requires current course reviews; newly authored
handoff drills remain separate from reserved assessment cases.

## Technical Evidence

Qualified machine: Apple M3 Max, macOS 26.6.2, Python 3.13.15,
python-tcod 21.2.1, SDL 3.2.16, Metal renderer. The bundled font is a
public-domain 8-by-10-cell atlas; its source and digests are in the
[font notice](assets/LICENSE.md).

| Check actually run | Result |
| --- | --- |
| Headless game tests: `python3 -B -m unittest discover -s tests -p test_packet_post.py -v` | 12 passed; boundaries, support history, staged visibility, course review gates, save recovery, keyboard controller, and synthetic campaign completion |
| `python3 -B -m unittest discover -s tests -v` | All 136 tests passed in 77 seconds |
| `python3 -B -m packet_post --check` | Eight missions and 27 decisions passed, with source cards readable |
| `python3 -B verification/check_packet_post.py --decode` | Both stored packet projections exactly matched fresh local TShark output |
| `work/offline-game-venv/bin/python -B verification/check_packet_post.py` | All mission stages, evidence scrolling, commit visibility, results, reflections, stamps, and menu scrolling rendered at 64x36, 88x44, and 130x65 |
| Same renderer check with `--window --screenshot work/packet-post-final.png` | Real desktop window passed with Metal; routing screenshot visually inspected |
| Fresh virtual environment installed with `--no-index --find-links work/game-wheels` | Installation and desktop rendering passed using only downloaded wheels |
| System Python without tcod | Help, list, and content checks passed; normal launch returned actionable dependency instructions |
| Unavailable SDL display driver and launch from an unrelated directory | Display failure produced recovery guidance without a traceback; module content check passed with an explicit repository import path |
| Course version and fingerprint comparison against planning baseline `e239183` | Course 3.1 content and fixture hashes unchanged |
| `python3 -B verification/package_course.py --output work/packet-post-course.tar.gz --journey` | 283 tracked files plus metadata packaged; course, game content, diagrams, curriculum, LLM fixtures, local links, doctor, exemplars, real-tool views, and both 36-phase course journeys passed |
| Extracted game renderer with the offline-installed environment | All eight missions rendered from an unrelated directory containing spaces, without Git metadata |

The game tests drive the same keyboard controller used by the SDL event
loop, including text entry, commit, cancel, hints, evidence, save/resume,
and window-close preservation. They do not represent a person playing.
Native UI automation could not run because computer-use permissions were
unavailable. Physical keyboard behavior, interactive window resizing,
Retina scaling preferences, readability, and accessibility still need a
human desktop check. The automated desktop check opens and presents frames;
it does not establish those usability results.

The source package includes the game, its assets, and verification code.
Python and installed dependencies are provisioned separately. Core course
and content checks require no tcod or display. A dedicated macOS CI job
installs tcod and performs offscreen rendering; that newly configured remote
job has not been run as part of this local verification.

## Offline Wheel Inventory

The tested download is specific to macOS ARM64 and Python 3.13. Wheels and
`SHA256SUMS` are retained under ignored `work/game-wheels/` on this machine.
The checksums below make this qualification reproducible; they do not imply
that these wheels support other interpreter/platform combinations. See the
[installation recipe](README.md#evidence-maintenance-and-packaging).

| Wheel | SHA256 |
| --- | --- |
| `attrs-26.1.0-py3-none-any.whl` | `c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309` |
| `cffi-2.1.1-cp313-cp313-macosx_11_0_arm64.whl` | `19ee6127ee34de7d83ce3d371ebc5ed91addbdcc39f9ab15ce4eb35a4e534971` |
| `numpy-2.5.3-cp313-cp313-macosx_14_0_arm64.whl` | `f9a2353b37a1a9e78fd82b27ad7e2a32a2d036604d18f02b05e3136c62ca3b09` |
| `pycparser-3.0-py3-none-any.whl` | `b727414169a36b7d524c1c3e31839a521725078d7b2ff038656844266160a992` |
| `tcod-21.2.1-cp310-abi3-macosx_10_13_universal2.whl` | `a481b535f93d0befd71721b198163e69217560a559b044dfb85cf50f1feaae02` |
| `typing_extensions-4.16.0-py3-none-any.whl` | `481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8` |

## Human Validation Still Required

Owner: facilitator, assisted by an independent technical reviewer and the
developer. No participant observations have been supplied for this game.
The owner's scheduled weekend work is recorded in the readiness gates above.
Existing course pilot and review work in the
[facilitator pilot worksheet](../facilitator/pilot.md) remains outstanding;
game checks do not close it.

1. Recruit about four to six beginners and experienced practitioners.
   Record prior networking and course exposure, platform, assistance, and
   accommodations. Use a short routing baseline and a different, equally
   difficult post-play item authored independently of game answers and
   reserved course exits.
2. Observe the Sorting Office without coaching the controls unless needed.
   Record time to first meaningful choice, navigation errors, hints, retries,
   abandonment, distracting jokes, and willingness to continue. Check narrow
   windows, all font sizes, plain tone, high contrast, text input, close/resume,
   and journal export with the participant's actual keyboard.
3. Ask for an explanation of longest-prefix matching, the complete eligible
   next-hop set, VRF scope, and what the selected route leaves unproved.
   Review mechanism, evidence, uncertainty, and next action independently
   of stamps or game feedback. Retain examples and counts, not unsupported
   effectiveness percentages from a small sample.
4. If comparing with the existing workbench, counterbalance activity order
   and use different equivalent items. Where feasible, collect another
   unseen transfer explanation several days later; record missing follow-up
   and prior exposure.
5. Have the independent reviewer inspect route eligibility, packet-size
   boundaries, clock limitations, source dependencies, staged case release,
   P1/P2 handoffs, and recovery claims. Check that the whimsical map suggests
   no unsupported physical link, policy result, or application outcome.
6. Resolve recurring control failures or misconceptions before calling the
   software classroom-qualified. Record findings, revisions, and follow-up
   observations. Only then consider replacing a named course activity while
   preserving teaching time and required artifacts.

Record each trial with this compact worksheet:

| Field | Observation |
| --- | --- |
| Participant code, date, experience, prior exposure | Pending |
| Baseline and unseen transfer item IDs | Pending |
| Device, keyboard, display settings, assistance | Pending |
| First-choice time, control friction, hints, retries | Pending |
| Mechanism / evidence / uncertainty / action examples | Pending |
| Misconception or distracting metaphor | Pending |
| Follow-up outcome and missing data | Pending |
| Reviewer, finding, change, recheck | Pending |

## Deliberate Release Boundaries

The owner authorized finishing the campaign while human validation remains
pending; expansion therefore preceded the plan's proposed learner gate.
This preview status makes that departure explicit.

The standalone `python -m packet_post` entry point preserves the course
hash. Linked course mutations, an additional `./course game` command, and
curriculum replacement are deferred until an explicit later release. Static
authored boards use no animations or timers. The campaign is deterministic;
repeating it is familiar practice, not a fresh independent assessment.

Intel Macs, Windows/Linux desktop rendering, screen-reader support, signed
app bundles, and installed-app distribution have not been qualified.
No network services, live captures, LLMs, or telemetry are used by play.

## Decision Review Register

Each decision below requires independent human review. The check focus is
a review request, not a completed review. In the staff packet, the authored
answers and explanations are separated from the blank independent-result
column. Reviewers must calculate first, compare second, cite the source,
and record disagreements and their resolution. No row is approved yet.

| Decision | Source(s) | Check focus | Reveal boundary | Reviewer / result / resolution |
| --- | --- | --- | --- | --- |
| `route.host` | labs/fixtures/routing/route-candidates.csv | Host specificity and eligible hop | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `route.remove` | labs/fixtures/routing/route-candidates.csv | Remove only host route; retain both equal next hops | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
| `route.vrf` | labs/fixtures/routing/vrfs.json | CORP default versus OT no match | Ungated practice; scene 3; expected values only after commit | Pending / pending / pending |
| `route.transfer` | packet_post/assets/practice-routes.csv | Nearby host mismatch and complete equal set | Ungated practice; scene 4; expected values only after commit | Pending / pending / pending |
| `route.limits` | labs/fixtures/routing/route-candidates.csv, labs/fixtures/routing/vrfs.json | Route selection leaves policy/return/service unproved | Ungated practice; scene 5; expected values only after commit | Pending / pending / pending |
| `parcel.plain` | labs/fixtures/challenges/transfer.pcap | 20+20 headers; 1160-byte limit | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `parcel.tcp-options` | labs/fixtures/challenges/transfer.pcap | 20+32 headers; 1148-byte limit | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
| `parcel.ip-options` | labs/fixtures/challenges/transfer.pcap | 24+32 headers; 1144-byte limit | Ungated practice; scene 3; expected values only after commit | Pending / pending / pending |
| `parcel.receipt` | labs/fixtures/challenges/transfer.pcap | Observed ICMP is not sender receipt or verified TLS | Ungated practice; scene 4; expected values only after commit | Pending / pending / pending |
| `bridge.predict` | labs/fixtures/routing/ospf.json | Remaining eligible neighbor is .3 | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `bridge.clock` | labs/fixtures/routing/route-events.jsonl | 80 ms logged interval is not service recovery | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
| `bridge.bgp` | labs/fixtures/routing/bgp.json | Accepted advertisements and local preference scope | Ungated practice; scene 3; expected values only after commit | Pending / pending / pending |
| `budget.policy` | labs/fixtures/architecture/traffic-flows.csv | Intended F3/F4 permission versus enforcement | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `budget.state` | labs/fixtures/architecture/failures.jsonl, labs/fixtures/architecture/wan.json, labs/fixtures/architecture/traffic-flows.csv | Two distinct choices and state dependency | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
| `budget.wan` | labs/fixtures/architecture/failures.jsonl, labs/fixtures/architecture/wan.json, labs/fixtures/architecture/traffic-flows.csv | Path choices leave measured capacity/loss unknown | Ungated practice; scene 3; expected values only after commit | Pending / pending / pending |
| `budget.twist` | labs/fixtures/architecture/failures.jsonl, labs/fixtures/architecture/wan.json, labs/fixtures/architecture/traffic-flows.csv | Shared power persists across transports | Ungated practice; scene 4; expected values only after commit | Pending / pending / pending |
| `crumbs.pattern` | labs/fixtures/incident/flows.jsonl, labs/fixtures/incident/siem.jsonl | Pattern and derived source dependencies; requests recorded | c05.review; scene 1; expected values only after commit | Pending / pending / pending |
| `crumbs.attribution` | labs/fixtures/incident/endpoint.jsonl, labs/fixtures/incident/auth.jsonl, labs/fixtures/incident/dns.jsonl | DNS attribution is not socket attribution; auth scope | c05.review; scene 2; expected values only after commit | Pending / pending / pending |
| `crumbs.clock` | labs/fixtures/incident/auth.jsonl | Normalize -06:00 to UTC without causal-order claim | c05.review; scene 3; expected values only after commit | Pending / pending / pending |
| `crumbs.boundary` | labs/fixtures/incident/firewall.jsonl, labs/fixtures/incident/proxy.jsonl, labs/fixtures/routing/vrfs.json | CORP source, one OT deny, proxy BYPASS scope | c05.review; scene 4; expected values only after commit | Pending / pending / pending |
| `handoff.predict` | No case evidence yet | Record two hypotheses before case release | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `handoff.attachment` | packet_post/assets/handoff.json | P1 VLAN intent and neighbor resolution, no repaired-service proof | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
| `handoff.action` | packet_post/assets/handoff.json | Evidence-linked owner, approved change, success test and rollback | Ungated practice; scene 3; expected values only after commit | Pending / pending / pending |
| `handoff.application` | packet_post/assets/handoff.json | P2 transport progress and remaining application failure | Ungated practice; scene 4; expected values only after commit | Pending / pending / pending |
| `recovery.receipt` | labs/fixtures/challenges/recovery.json | Hypothetical RA scoped acceptance and RB unresolved service | c06.review, exit.review; scene 1; expected values only after commit | Pending / pending / pending |
| `foundation.envelopes` | labs/fixtures/pcaps/foundations.pcap, labs/fixtures/network/dhcp.jsonl | Next-hop MAC versus final IP within capture scope | Ungated practice; scene 1; expected values only after commit | Pending / pending / pending |
| `foundation.directory` | labs/fixtures/network/troubleshooting.json | NXDOMAIN response versus timeout; HTTP 503 after DNS/TCP | Ungated practice; scene 2; expected values only after commit | Pending / pending / pending |
