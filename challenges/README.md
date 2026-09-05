# One-Day Network Bootcamp

You are taking over a shift on a fictional factory's operations team. Keep
approved services available, investigate a transfer failure, then decide what
the evidence supports about suspicious activity. The outage drills and the
incident are separate episodes on the same network.

**Six teaching hours; seven elapsed hours with lunch and breaks.** Work in
pairs, remotely, or alone. You need no previous vendor configuration experience.
Install and check the [prerequisites](../prerequisites/README.md) beforehand;
installation is additional time. All required evidence is local.

Open `./course` for the guided route, `./course day` for this overview, or
`./course challenge 1` for the first brief. The module commands still open the
reference library. No progress data or learner answers are stored by the CLI.

## Start the Shift — 15 Minutes

1. Write a private first prediction: “A dashboard opens, but a transfer stalls.
   My first hypothesis is [write it]; I would request [evidence] because [reason].”
2. Without looking anything up, answer: is `10.0.10.53` local to
   `10.0.10.23/24`? Does resolving a name prove its server is reachable? What
   does a completed TCP handshake prove about an application?
3. Inspect this decoded observation from the transfer drill: packets 1–3 show
   SYN, SYN-ACK, ACK between `10.0.10.23` and `203.0.113.20:443`. Revise one
   hypothesis. Which unanswered question matters next?

No score yet. Consult the [reference card](reference.md) for unfamiliar terms.
The factory and its service requirements are fictional; the captures are
constructed teaching evidence, not records of a real attack.

## Prepare Three Deliverables

Run from the repository root. Copy each template only once; return to your
existing files on later sessions. These commands preserve existing answers.

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

Each deliverable is reviewed for mechanism, cited evidence, uncertainty, and a
useful next action. Score each dimension 0–2: missing/unsupported, partial, or
demonstrated. Aim for 6/8 with no zero after feedback and revision, and explain
the individual exit case. The full rubric and worked examples are in the
[facilitator guide](../facilitator/README.md#assessment).

Exact-answer workbench quizzes are optional practice, not the final grade.
Open the [worked solutions](../facilitator/solutions.md) after your attempt.
These materials use an ordinary reveal convention; nothing is locked.

The [104 reference guides](../modules/README.md) remain available for deeper
reading. Their individual submission instructions are optional extended-study
exercises; the one-day course requires only the three deliverables above.
Try [extensions](extensions.md) after the required day.
