# Packet Post Validation Record

## Release Status

Software preview, September 17, 2026. Eight missions contain 27 authored
decisions. The requested software implementation is complete; observed
learner trials and independent human review remain pending by the project
owner's explicit decision. No learning-effectiveness claim, curriculum
replacement, or independent attainment follows from these technical checks.

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
| Course version and fingerprint comparison against planning baseline `e239183` | Course 3.1 content and fixture hashes unchanged |
| Extracted source archive verification and real-tool course journeys | Pending final packaging run |

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
developer. No participants have been recruited or observed for this game.
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
