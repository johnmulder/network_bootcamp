# Facilitate the One-Day Bootcamp

Teach the [one-day route](../challenges/README.md), using the
[agenda](../agenda.md) as the curriculum contract. The old subsection guides
are optional reference exercises. Require three deliverable bundles, not a
submission for each of the 104 guides.

## Before the Session

- Send the prerequisites in advance; allow separate installation support time.
  Run `./prerequisites/setup.sh --check` and `./course verify`.
  Zeek/iperf3 reference exercises additionally use setup with `--extended`.
- Have each participant copy the three templates and existing ledger CSV using
  the one-day start instructions. Never overwrite prior learner work.
- Prepare endpoint cards or use the equivalent text tables. Pair learners and
  rotate the person making a decision and the person requesting evidence.
- Reserve one capstone case for the individual exit task. Default: A for the
  group, B for the exit. Avoid opening the reserved solution prematurely.
- Open [solutions and provenance](solutions.md) separately from student briefs.
  Filenames and reveal points are teaching conventions, not access controls.
- Prepare the [pilot worksheet](pilot.md); distinguish rehearsal findings from
  observations made with actual learners.

The fictional factory supplies a purpose, not a claim that every failure is
part of one attack. Explicit drill conditions take precedence within their
case only. Keep the original incident, route exercises, and capstone variants
separate when participants make causal claims.

## Facilitation Rhythm and Timing

The student schedule totals 360 teaching minutes plus 60 minutes of breaks and
lunch. Preserve all breaks and the exit/debrief. Aim for at least 210 minutes
of participant prediction, inspection, explanation, or discussion.

| Block | Teaching minutes | Planned active minutes | Reveal / facilitation cue |
| --- | ---: | ---: | --- |
| Opening | 15 | 10 | Record a prediction, then show one decoded handshake observation. |
| Be the Packet | 65 | 45 | Model one hop; let learners trace before checking the CSV variation. |
| Transfer | 45 | 35 | Do not name the diagnosis; reveal packet-size evidence after hypotheses. |
| Pull One Link | 40 | 30 | Freeze at failure, then reveal the event sequence. |
| Resilience Budget | 60 | 45 | Record token choices before outcomes and the shared-power twist. |
| Suspicious Is Not Proven | 65 | 50 | Release one round every 12 minutes; ask what changed in confidence. |
| Handoff | 55 | 40 | Pairs exchange simultaneously; solo learners use the rubric. |
| Exit | 15 | 10 | Five minutes alone, five reviewing, five feedback. |
| **Total** | **360** | **265** | **Verify actual times during the pilot.** |

Explain concepts in segments of at most ten minutes, then require a decision.
If time slips, remove optional vocabulary tours and quiz repetitions. Do not
remove evidence inspection, return-path reasoning, or debriefing to preserve
the number of topics mentioned.

## Use the Opening Diagnostic

The local-address question checks whether `/24` is meaningful to the learner.
The DNS question checks dependency confusion; the handshake question checks
overclaiming. No experience is assumed beyond willingness to use the supplied
commands. Start with the pocket reference and the first worked hop if needed.

If most learners struggle, spend the recognition-tour time on these foundations.
If one person is experienced, ask them to explain an evidence limitation rather
than race ahead through the answers. Do not let one terminal operator supply
all explanations for a pair.

Use a private first prediction, pair discussion, and revision. Welcome “I
changed my mind because this field contradicts my first idea.” Do not reward
speed, confident guesses, or the most dramatic attack story. Offer hints
without penalty and accept written alternatives to role-play or speaking.

## Assessment

Apply this rubric to the three artifact bundles and to the capstone. The
incident bundle includes the existing ten-field CSV. A score is a feedback
aid, not a certification of operational competence.

| Dimension | 0 — Needs revision | 1 — Developing | 2 — Demonstrated |
| --- | --- | --- | --- |
| Mechanism | Names a symptom only or gives a wrong mechanism | Explains part of the path | Explains forwarding, policy/state, and relevant return or failure behavior |
| Evidence | Unsupported conclusion | Relevant source without precise linkage | Exact records/fields support the claim with clear provenance |
| Uncertainty | Treats assumptions as facts | Names a limitation | Gives a plausible alternative or unresolved question and discriminating evidence |
| Action and handoff | Vague or unjustified action | Useful action with incomplete validation | Proportionate step with owner, validation, and rollback where applicable |

Completion: at least 6/8 with no zero after feedback and revision, and an
individual explanation of the changed flow in the exit case. The rubric does
not require a particular wording or a single architecture choice. A learner
who correctly leaves a claim unresolved can earn full credit.

### Sample Graded Responses

| Response | Mechanism / evidence / uncertainty / action | Feedback |
| --- | --- | --- |
| “The network is down. Restart the firewall.” | 0 / 0 / 0 / 0 | Identify the affected flow and an actual observation before prescribing a change. |
| “A3 says the return packet has no route. Restore the route.” | 2 / 2 / 0 / 1 = 5 | Explain the missing intent information; name an owner, validation, and rollback. |
| “In A-v1 the forward `/8` still reaches on-prem, but the return `/16` is absent. A2 shows a server reply; A3 records its route drop. The change's intent is unknown. Network operations should check the change record and restore the authorized return route if unintended, verify TCP plus the TLS health request, and roll back if validation fails.” | 2 / 2 / 2 / 2 = 8 | Clear mechanism, provenance, limit, and owned action. |

Score before and after revision separately. For incident scope, distinguish
observed activity on a host from confirmed compromise of that host. A successful
authentication does not prove credential theft or remote code execution.

## Solo and Remote Delivery

Every challenge supports written answers and a self-review path. Solo learners
record a prediction before reading the next round, then use hints or solutions.
In remote groups, share the text tables and case IDs; no physical cards or
screen-color distinctions are required. All pairs can exchange handoffs at
once; do not add class-size-dependent presentation time.

## Pilot and Improvement

See the [implementation validation record](validation.md) for completed
technical checks and the learner outcomes that remain unmeasured.

Run an actual pilot when learners are available. Record beginner/experienced
and solo/pair modes without collecting unnecessary personal data. Target
80% meeting the rubric after one revision and median 4/5 on both engagement
questions. These are targets, not existing results.

If engagement is high but reasoning shallow, improve evidence prompts. If the
day overruns, shorten optional surveys and repeated reporting. Use the
[pilot worksheet](pilot.md) to preserve findings and follow-up decisions.
