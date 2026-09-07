# One-Day Network Bootcamp

You are taking over a shift on a fictional factory's operations team. Keep
approved services available, investigate a transfer failure, then decide what
the evidence supports about suspicious activity. The outage drills and the
incident are separate episodes on the same network.

**Six teaching hours; seven elapsed hours with lunch and breaks.** Work in
pairs, remotely, or alone. You need no previous vendor configuration experience.
Install and check the [prerequisites](../prerequisites/README.md) beforehand;
installation is additional time. All required evidence is local.

Open `./course` for saved guided delivery, or use
`./course learn --id my-session`. The runner creates a workspace and preserves
accepted answers between sessions. `./course day` shows this manual overview;
`./course challenge 1` prints a complete brief. The module commands still open
the reference library. Manual browsing does not record completion.

## Start the Shift — 15 Minutes

<!-- delivery:start opening.predict -->
Write a private first prediction: “A dashboard opens, but a transfer stalls.
   My first hypothesis is [write it]; I would request [evidence] because [reason].”
<!-- delivery:end opening.predict -->

<!-- delivery:start opening.diagnostic -->
Without looking anything up, answer: is `10.0.10.53` local to
   `10.0.10.23/24`? Does resolving a name prove its server is reachable? What
   does a completed TCP handshake prove about an application?
<!-- delivery:end opening.diagnostic -->

<!-- delivery:start opening.reflect -->
Inspect this decoded observation from the transfer drill: packets 1–3 show
   SYN, SYN-ACK, ACK between `10.0.10.23` and `203.0.113.20:443`. Revise one
   hypothesis. Which unanswered question matters next?

The diagnostic has no rubric score. Use factual feedback to correct your
answers before continuing. Consult the [reference card](reference.md) for
unfamiliar terms.
The factory and its service requirements are fictional; the captures are
constructed teaching evidence, not records of a real attack.
<!-- delivery:end opening.reflect -->

## Prepare Three Deliverables

Guided delivery creates these files under `work/<session-id>/` automatically.
For manual study, run the following from the repository root. Copy each
template only once; return to your existing files on later sessions. These
commands preserve existing answers. Keep manual and guided workspaces separate.

```sh
mkdir -p work/bootcamp
cp -n challenges/templates/packet-path.md work/bootcamp/packet-path.md
cp -n challenges/templates/architecture.md work/bootcamp/architecture.md
cp -n challenges/templates/incident.md work/bootcamp/incident.md
cp -n labs/fixtures/incident/evidence-ledger-template.csv work/bootcamp/evidence-ledger.csv
./course verify
```

The CSV belongs to the incident deliverable. Use a text editor for Markdown;
the CSV can be edited as plain text or in a spreadsheet. Quote CSV cells that
contain commas. Do not put answers inside `labs/fixtures/`.

## Follow the Day

| Time | Minutes | Challenge | Update |
| --- | ---: | --- | --- |
| 09:00–09:15 | 15 | Start the Shift, above | First prediction |
| 09:15–10:20 | 65 | [1. Be the Packet](01-be-the-packet.md) | Packet path |
| 10:20–10:35 | — | Break | |
| 10:35–11:20 | 45 | [2. The Transfer That Stops](02-the-transfer-that-stops.md) | Diagnosis |
| 11:20–12:00 | 40 | [3. Pull One Link](03-pull-one-link.md) | Failure timeline |
| 12:00–12:30 | — | Lunch | |
| 12:30–13:30 | 60 | [4. Spend Your Resilience Budget](04-resilience-budget.md) | Architecture |
| 13:30–14:35 | 65 | [5. Suspicious Is Not Proven](05-suspicious-is-not-proven.md) | Incident dossier |
| 14:35–14:50 | — | Break | |
| 14:50–15:45 | 55 | [6. The Shift Handoff](06-the-shift-handoff.md) | All three |
| 15:45–16:00 | 15 | Individual exit task in Challenge 6 | Feedback and revision |
| **Teaching total** | **360** | **Breaks and lunch: 60 minutes** | |

Predict before revealing the next evidence. In pairs, alternate choosing the
next check and explaining why it matters. Solo learners write the explanation
before opening the next section. Request [hints](hints.md) freely; changing
your mind and acknowledging uncertainty are part of the work.

## Completion

Follow the [completion policy](../agenda.md#completion-and-feedback): finish the
required phases and artifacts, independently correct the required factual
checkpoints, and record seven current reviews, one for each challenge and the
individual exit. Each review needs 6/8 with no zero for mechanism, evidence,
uncertainty, and action. Self-review and facilitator review are reported
separately. The [facilitator guide](../facilitator/README.md#assessment) explains
the rubric.

Hints and corrections are encouraged. If you reveal a worked answer before
correctly answering a checkpoint, you can still finish the activities and
improve your rubric scores, but that answer remains demonstrated rather than
independent. The session then records delivery finished without independent
completion. Keep that history; the completion policy explains separate
reassessment. Reaching the end or earning a passing rubric score alone does
not establish course completion.

Standalone workbench quizzes are optional practice, not the required factual
checkpoints in guided delivery.
Open the [worked solutions](../facilitator/solutions.md) after your attempt.
These materials use an ordinary reveal convention; nothing is locked.

The [104 reference guides](../modules/README.md) remain available for deeper
reading. Their individual submission instructions are optional extended-study
exercises; the one-day course requires only the three deliverables above.
Try [extensions](extensions.md) after the required day.
