# Packet Post: The Night Shift

A whimsical, offline networking practice game in a python-tcod desktop
window. Join the Brambleworks Packet Post, make a prediction, change a
bounded condition, inspect evidence, and leave a useful note for the next
shift. All controls work with a keyboard. Nothing is timed.

**Status:** software preview; learner trials and independent human review
remain pending. See the [validation record](VALIDATION.md). Postage stamps
record practice, not course completion or independent attainment.

## Student Start Card

Your facilitator provides a prepared Mac, a course folder, and an individual
save ID. This preview is for supervised practice while student validation
is pending. Installation happens before the session. Ask the facilitator
to open Terminal in the supplied course folder, then use your assigned ID:

```sh
work/game-venv/bin/python -m packet_post --id student-01
```

Use that same folder and ID next time. A different folder has separate saves.
The window contains a text grid; it is separate from Terminal.

1. Choose **The Sorting Office** with the arrow keys and press Enter
   (Return on a Mac). If local versus remote delivery is unfamiliar, ask
   to begin with **Two Envelopes & the Directory Desk**, mission 8.
2. Read the brief and press Enter. Press **E**, then a source's number,
   to inspect evidence. Use Up/Down to scroll and Escape to return.
3. Move through the answer fields with arrows or Tab. Enter or Space
   selects an option; `[x]` means selected. Some fields need several options.
   Keep moving down: the form scrolls to reach the reason and commit action.
4. On **My reason**, press Enter, type your explanation, then press Enter
   to keep it. Backspace erases from the end; Escape cancels that edit.
   Command letters are ordinary text while you type.
5. Select **Commit prediction** only when every field and your reason are
   ready. Press **V** after feedback to compare your prediction with the
   complete result. Escape closes the result. Use **R** to revise or Enter
   to continue after a factual match. Malformed input does not use an attempt.
6. Use **H** when a learning hint would help. Enter confirms the hint;
   Escape cancels before it opens. Hints and retries record support and
   cost no stamp. The first attempt remains in your journal.
7. Finish the four debrief notes: explain the rule, cite evidence, identify
   an unknown, and propose the next check with its owner and success
   condition. Select **Save reflection & collect stamp**. Your prose is
   saved for review; the game does not grade its quality.

Press **?** for controls. F2 switches tone, F3 changes contrast, and F4
cycles text size. On keyboards using media controls, try holding Fn or
Globe with the function key; ask the facilitator if the setting does not
change. The keyboard/display setup still needs qualification for your class.

Escape returns from a mission to the desk. At the desk, **Q** quits. Start
again with the same ID to resume. **J** reads the journal; **X** exports it
and shows the new file's path under `work/packet-post/<id>/`. Exports contain
your written answers. Share one only when you intend to share that work.

If an action reports a save error, stop and ask the facilitator. A failed
text save keeps your edit open: Escape dismisses the error, then Enter
retries saving. A second Escape cancels the edit. A failed option selection
returns to its previous saved value. Do not force-quit to clear a save error.

**After course review** means the mission uses material intended for later
practice. Ask the facilitator when it becomes available. A stamp confirms
practice; it does not replace the course's assessment or prove service
recovery. Nothing is timed, and you can pause or ask for help.

If the text grid is difficult to use, tell the facilitator before starting.
They can arrange suitable practice using the existing course/workbench and
check that the alternative works for your needs.

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

## Facilitator Runbook

This is an optional preview. Name the mission(s) assigned for the session;
do not describe all eight as classroom-qualified while the
[readiness gates](VALIDATION.md#student-readiness-gates) remain pending.
Assign a facilitator contact, provision devices before teaching time, and
use one anonymous save ID per participant, including partners. Keep any
raw observations and learner journals under ignored `work/`.

### Choose the Practice

| Order | Mission | Prerequisite and teaching focus |
| --- | --- | --- |
| As needed | Foundations (8) | Basic addresses; work through local/remote delivery, neighbor MAC, and DNS/application boundaries |
| 1 | Sorting (1) | Matching prefixes and reading a route table; reason about scope and eligible sets |
| 2 | Parcel (2) | Add headers and payload; separate fitting the MTU from a successful transfer |
| 3 | Bridge (3) | Read route/event records; distinguish installation time from application recovery |
| 4 | Resilience (4) | Recognize service dependencies and policy intent; defend a two-token tradeoff |
| 5 | Suspicious Crumbs (5) | Complete current `c05.review`; reason across staged sources without overclaiming attribution |
| 6 | Handoff (6) | Read supplied evidence and name owners, tests, and rollback; these are new P1/P2 practice drills |
| 7 | Return Receipt (7) | Complete current `c06.review` and `exit.review`; evaluate scoped service restoration |

The menu remains freely navigable except for the two post-course gates.
Use mission names or their menu numbers, not the order column as a shortcut.
Published durations are estimates awaiting observed trials. Schedule this
practice outside the required 360-minute course until a specific replacement
has been reviewed. It does not change the course's required artifacts.

### Before Students Arrive

1. Keep the source archive, wheel hashes, Python/OS versions, and matching
   course/game copy together. The prepared readiness bundle includes exact
   dependency requirements for its stated Mac/Python target. Follow its
   installation instructions and verify hashes before use.
2. Open each teaching Mac with its actual student keyboard and display.
   Check launch, an editable reason, readable evidence, all font sizes,
   contrast, and the Fn/function-key combinations. If any student needs an
   alternative interaction, rehearse appropriate course/workbench practice
   with that student; journal export is not an accessibility substitute.
3. Confirm a harmless trial ID can save, close, reopen, and export. Do not
   use a participant's ID for this rehearsal. Keep the previous matching
   copy so a content-version change never strands existing work.
4. For eligible students, add `--course-session THEIR-COURSE-ID` to launch.
   A game ID and course-session ID are separate. Check current valid reviews
   through the course's existing interface; never manufacture them or edit
   state files. Reopening without this flag keeps gated missions locked.
5. Give students the start card and an assigned ID. Explain whom to contact,
   which mission to select, and where exports are stored. A Terminal opened
   in the correct course folder removes avoidable path navigation.

### Recover Without Losing Work

| Symptom | Facilitator action |
| --- | --- |
| `No module named packet_post` | Return to the supplied course folder and use its prepared interpreter; the game module needs the repository on Python's import path |
| Optional tools missing | Use the prepared virtual environment; provision the exact supplied wheels before class, then rerun the start command |
| Display cannot open | Launch from the local desktop; keep the save and use the agreed course alternative if that Mac cannot render |
| Save is open elsewhere | Close the other game process using that same ID; do not delete lock files or launch competing writers |
| Directory is not a game save | Preserve it and choose another assigned ID; never replace unrelated files |
| Storage error while editing | Keep the game open, restore available space/write permission, dismiss the error with Escape, and press Enter to retry; cancelling the edit discards its unsaved text |
| Malformed or changed-version save | Close the game, copy the complete save folder for safekeeping, and use the matching original course/game copy to resume/export; if unavailable, preserve the original and use a new ID |
| Locked incident/recovery mission | Check the participant's own course reviews and launch flag; do not bypass release rules |
| Export seems absent | Read the new filename shown by X, or use the headless export command below; every export has a distinct name |

With the game closed, export a valid save without opening a window:

```sh
python3 -B -m packet_post --id student-01 --export
```

For recovery in a different matching course copy, copy the entire closed
`work/packet-post/<id>/` folder, including its hidden `.packet-post` marker,
into that copy's `work/packet-post/`. Preserve the original and use an empty
destination; do not merge two students' saves. Both copies must match the
saved content version. Deleting the lock file does not repair a save.

During a trial, record observations and assistance using the
[course pilot conventions](../facilitator/pilot.md). Stop for lost work,
an unresolved blocker, or materially wrong teaching feedback. Preserve the
finding and the candidate version, then use the agreed alternative activity.
The next cohort uses the repaired version only after the failed check has
been repeated successfully. Do not change a student's version mid-session.
