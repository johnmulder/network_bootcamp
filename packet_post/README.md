# Packet Post: The Night Shift

A whimsical, offline networking practice game in a python-tcod desktop
window. Join the Brambleworks Packet Post, make a prediction, change a
bounded condition, inspect evidence, and leave a useful note for the next
shift. All controls work with a keyboard. Nothing is timed.

**Status:** software preview; learner trials and independent human review
remain pending. See the [validation record](VALIDATION.md). Postage stamps
record practice, not course completion or independent attainment.

## Install and Play

From the repository root, use Python 3.10 or later. The qualified desktop
configuration is macOS on Apple Silicon with Python 3.13 and tcod 21.2.1.
Install these optional dependencies before going offline:

```sh
python3 -m venv work/game-venv
work/game-venv/bin/python -m pip install -r requirements-game.txt
work/game-venv/bin/python -m packet_post
```

This opens a desktop window with a character grid; it does not run inside
your terminal. Core course commands need no tcod installation. The game
never opens a network connection, runs arbitrary commands, changes device
configuration, or calls an LLM. All evidence is saved teaching material.

Use a different local save name for another participant:

```sh
work/game-venv/bin/python -m packet_post --id another-shift
```

Read the mission list, check content, or export a journal without tcod or a
display:

```sh
python3 -B -m packet_post --list
python3 -B -m packet_post --check
python3 -B -m packet_post --id night-shift --export
```

Module launch requires the repository root on Python's import path. For a
launch from another directory, set `PYTHONPATH` to that root and invoke its
virtual-environment Python; assets and saves resolve against the repository,
not your shell's current directory.

## Missions

| Mission | What you do |
| --- | --- |
| The Sorting Office | Select prefixes and complete next-hop sets; remove a host route; compare VRFs; apply the rule to a new authored table |
| The Parcel That Wouldn't Fit | Choose a payload and predict the header-inclusive size against the IP MTU |
| The Bridge on Tea Break | Predict a remaining path, reconstruct the recorded interval, and compare supplied BGP attributes |
| Two Tokens and a Teapot | Choose two improvements, compare modeled dependencies and risks, and confront a shared-power twist |
| The Case of the Suspicious Crumbs | Request staged incident sources, qualify claims, normalize a timestamp, and preserve source dependencies |
| Please Forward to the Next Shift | Diagnose new game-only P1/P2 drills and write a short handoff |
| Return Receipt Requested | Compare hypothetical post-assessment service tests and owner decisions |
| Two Envelopes & the Directory Desk | Optional foundations: next-hop MAC versus final IP, and DNS versus application failure |

The original incident and recovery material are post-lesson practice. To
unlock them, supply a guided-course session with current passing reviews:

```sh
work/game-venv/bin/python -m packet_post --course-session bootcamp
```

Incident practice requires `c05.review`. Recovery requires both
`c06.review` and `exit.review`. Either a current self-review or facilitator
review suffices for this reveal convention. The game reads these statuses;
it never changes course answers, reviews, or completion. There is no bypass
flag. The other missions, including new handoff drills, work without a
course session. The game never draws from reserved A/B cases or course
reassessment variants.

## Controls and Learning

| Key | Action |
| --- | --- |
| Arrows / Tab / Shift+Tab | Move through missions or fields |
| Enter / Space | Select an option, edit a field, or activate the highlighted action |
| Number at desk | Open that mission |
| E | Choose an evidence card by number |
| H | Offer a recorded learning hint; Escape cancels before exposure |
| B | Show the full logical decision board |
| V after feedback | Read the full scrollable prediction/result comparison |
| R after feedback | Make a supported retry without erasing the first attempt |
| J / X | Read / export the journal |
| Escape | Close a panel or return to the desk |
| Q at desk | Quit |
| F2 / F3 / F4 | Plain tone / high contrast / font size |
| ? | Read controls without answer exposure |

In the text editor, Enter keeps the text and Escape cancels that edit.
Command letters are ordinary text while editing. Evidence and result panels
support arrows, Page Up/Down, Home, and End. Smaller windows use a single
decision panel; B keeps the full board available. No animation, sound,
mouse, or speed-dependent task is required.

Complete each field and add a reason before choosing **Commit prediction**.
Malformed inputs do not consume an attempt. Feedback shows the expected
bounded facts; any subsequent retry is supported practice. Changing your
mind is useful work, not a penalty. The final four notes cover mechanism,
evidence, uncertainty, and action. Handoff notes total at most 150 words.
The game stores prose without grading its quality.

A map is a logical decision board. Cursor movement does not transmit a
packet, reduce TTL, or change a real network. A route selection is not proof
of policy permission or application recovery. A fitting packet establishes
only the size condition. In a budget mission, valid token choices are
recorded choices; no pair automatically earns a successful-service claim.

The graphical grid has not been qualified for screen readers. Text journal
exports and the existing line-oriented course remain available. Human
accessibility and usability evaluation is still pending.

## Saves and Recovery

Practice lives under `work/packet-post/<id>/`. Committed actions, hints,
opened cards, completed text edits, selections, and reflections persist.
The window-close handler also saves the current text edit. An abrupt
process kill can lose text typed since its last saved edit, but cannot
replace the prior save with a partial JSON write.

Only one process can write a save. Unrelated directories and symlink saves
are rejected. Invalid or changed-version saves are preserved with recovery
instructions. Restore the matching game/course copy to resume them, or use
a new ID. There is no silent migration or reset. Repeating known puzzles
in another save remains practice, not fresh course attainment.

Each journal export uses a new filename. Journals contain learner text,
predictions, support history, bounded results, and sources. They stay local;
review them before sharing. The game does not overwrite course artifacts.

## Evidence, Maintenance, and Packaging

Rules reuse the course's route helpers, factual evaluator, and finite
experiments. Scenes use their own visibility rules. Different route tables,
factory captures, incident records, and independent drills retain their
own scopes. Evidence cards retain source names and original record/frame
numbers. A derived view is labeled with its original input.

The [saved packet views](assets/observations.json) include original frame
numbers, capture SHA256, TShark version, and exact decoder arguments. Normal
play verifies the parent hash and reads this local projection; it does not
need TShark. Maintainers with course tools can compare it with a fresh decode:

```sh
python3 -B verification/check_packet_post.py --decode
```

The [bundled font notice](assets/LICENSE.md) records the public-domain source
and atlas hashes. No asset download occurs during play.

Run content and behavioral checks without game dependencies, then renderer
checks using the game environment:

```sh
python3 -B -m unittest discover -s tests -p test_packet_post.py -v
python3 -B verification/check_packet_post.py --content
work/game-venv/bin/python -B verification/check_packet_post.py
work/game-venv/bin/python -B verification/check_packet_post.py --window
```

The course packager includes tracked game sources and assets and checks
extracted content without tcod. A source archive does not bundle Python or
installed dependencies. For an offline classroom on the same platform and
Python version, prepare a wheel directory before disconnecting:

```sh
work/game-venv/bin/python -m pip download --only-binary=:all: -r requirements-game.txt -d work/game-wheels
python3 -m venv work/offline-game-venv
work/offline-game-venv/bin/python -m pip install --no-index --find-links work/game-wheels -r requirements-game.txt
```

Record the wheel filenames, SHA256 digests, platform, and Python version
for a distributed classroom bundle; provision each target configuration
separately. The repository's CI keeps core tests independent of tcod and
adds a separate macOS offscreen-render job.

The standalone launch preserves the existing course content hash. A future
`./course game` command, linked course mutation, app bundle, additional
platform support, or added required classroom time needs its own release
decision after learner feedback.
