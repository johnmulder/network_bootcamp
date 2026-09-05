# The Shift Handoff

> Integrated capstone · 55 minutes, then a 15-minute individual exit block

A fresh service problem arrives before the next shift. Use your three
deliverables to analyze it without a prescribed sequence of commands.
Prerequisite: complete Challenges 1–5, with hints and revisions as needed.

## Receive the Case — 5 Minutes

Choose **A** for the team capstone; reserve **B** for the individual exit task.
A facilitator may reverse them, but do not read the reserved case early.

```sh
jq '.' labs/fixtures/challenges/case-a.json
```

Case packets are small independent drills dated the following day, not extra
events in the original incident. Their explicit conditions replace relevant
reference assumptions for that drill only. Route snapshots are complete for
the specified flow; that does not assert global knowledge of the network.

## Analyze — 20 Minutes

Use the case's flow, before/after state, policy conditions, and observations.
Update each deliverable under a heading with the exact case ID:

- **Engineering:** Trace forward and return decisions. Name the specific
  change, table, and observation that explain the behavior.
- **Architecture:** Mark the affected boundary and service. Distinguish the
  changed dependency from services that the case does not show failing.
- **Security:** Separate stated permission from actual enforcement. Determine
  whether a deny, translation, or missing forwarding decision is evidenced.
- **Response:** State the supported mechanism, uncertainty about intent or
  scope, best next action, and owner.

In pairs, each learner covers two viewpoints, then swaps explanations. Alone,
write one sentence from each viewpoint. Use case-specific observation IDs in
the ledger; do not merge the drill with the earlier incident timeline.

## Prepare the Handoff — 10 Minutes

Give the next shift an observation, impact, evidence, confidence, and next
step. Include the relevant return path, an alternative explanation or unknown,
validation, and rollback. Keep the spoken handoff under two minutes or the
written version under 150 words.

## Exchange and Challenge — 10 Minutes

Pairs exchange simultaneously. The recipient must state the next check in
their own words and identify an unsupported claim or missing qualification.
Solo learners compare against the [rubric](../facilitator/README.md#assessment)
before opening the relevant [solution](../facilitator/solutions.md#challenge-6).

## Debrief — 10 Minutes

Score mechanism, evidence, uncertainty, and action/handoff from 0–2. Revise
one weak dimension. Pass at 6/8 with no zero after feedback, plus the individual
exit explanation. Multiple proportionate actions may satisfy the rubric.
Useful [hints](hints.md#challenge-6) remain available without penalty.

## Individual Exit and Feedback — Additional 15 Minutes

Work alone for the first five minutes on the reserved case:

```sh
jq '.' labs/fixtures/challenges/case-b.json
```

In four sentences, state the changed path, cite a decisive record, say what
does not follow from it, and choose the next action. If your group used B,
use A instead. Take five minutes to compare with the relevant solution and
revise; use the remaining five for feedback and choosing a next topic.

Rate 1–5: “I wanted to find out what happened next” and “The challenge felt
manageable.” Name one activity that dragged and one place needing more
explanation. Facilitators record timing and results on the
[pilot worksheet](../facilitator/pilot.md).

You have completed the required path. The [extensions](extensions.md) and
[reference library](../modules/README.md) are optional next steps.
