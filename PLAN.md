# Bootcamp Engagement and Depth Plan

Status: proposed curriculum changes; implementation has not started.

## Recommendation and Scope

Turn the course into a day on a fictional operations team: trace a working
service, investigate a failure, defend a design decision, and assess a possible
incident. Keep the existing network, local evidence, three-module progression,
and emphasis on defensible reasoning.

The user-confirmed budget is **six teaching hours in one day**, with lunch and
breaks additional. The 104 guides become a reference library supporting an
explicit short path. Students finish three connected artifacts instead of
treating every guide as a separate assignment.

Increase depth through prediction, mechanism, changing conditions, and evidence
selection. Spend less class time enumerating technologies. Every required
concept should contribute to a decision students actually make.

This document proposes changes. [agenda.md](agenda.md) remains the authoritative
curriculum until implementation updates it. The completed navigation work from
the previous plan is retained at the end of this document.

## Review Findings

The review covered the agenda, setup and navigation documentation, all three
workbench guides, fixture examples, a structural scan of all 104 guides, and
close reading of representative lessons, exercises, and completion standards.

### Preserve These Strengths

- One fictional network connects forwarding, architecture, and investigation.
- Reproducible saved evidence supports substantial exercises on one Mac.
- Prediction, return paths, uncertainty, and communication are already central.
- Workbenches already offer feedback, retries, and reproducible practice.
- The incident has useful ambiguity: temporary egress permission, periodic
  traffic, successful authentication, and a denied OT attempt.

### Change These Friction Points First

| Finding and evidence | Likely student experience | Change |
| --- | --- | --- |
| All 104 guides require a separate submission, a falsifiable prediction, and at least three cited observations. Even the [opening objectives guide](modules/module-01-operational-networking/section-01-introduction-and-mental-model/01-course-objectives-and-shared-language.md) follows this format. Together, the guides contain about 50,000 words. | Repeated administration competes with discovery; the short path is unclear. | Keep rigorous evidence requirements at module checkpoints; use sketches, short predictions, and discussion between them. |
| The agenda and subsection guides lack a timed teaching path. | Breadth can consume the day before the integrated investigation. | Publish the six-hour schedule below and distinguish practiced skills from recognition-level topics. |
| Every guide exposes expected evidence alongside the task. The [investigation introduction](modules/module-03-incident-response-and-integration/section-04-investigation-exercise/01-scenario-and-evidence-set.md) states the main findings. | Students can repeat an explanation without making the investigative decision. | Separate challenge briefs from worked solutions; reveal explanations after an attempt. |
| Workbench seeds change question order, not the case. Several questions retrieve one fixture field. | Repeat scores can reflect familiarity rather than transfer. | Keep these quick checks; add a few authored variants that change the correct decision. |
| The [VXLAN/EVPN guide](modules/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md) requests VNIs, tunnel endpoints, and overlay mappings, but its commands inspect cloud route tables. | Students cannot support the requested analysis with the supplied evidence. | Make this a conceptual reference in the short path. Add appropriate evidence only for a later extension. |
| The [failure fixtures](labs/fixtures/architecture/failures.jsonl) already name affected entities, and the [workbench examples](modules/module-02-network-architecture/workbench/README.md) explain the result. | A useful explanation becomes a lookup exercise. | Ask students to predict affected flows before revealing outcomes. |

These are design judgments to test in a pilot, not measured claims about the
current students' engagement or learning.

## Technical Priorities

The promise remains practical fluency for technical collaborators. Students
should explain a mechanism, support a claim, and choose an informative next
step. Retain the following core, with explicit depth checkpoints.

| Core concepts | Required practice | Demonstration of depth |
| --- | --- | --- |
| Ethernet, MAC, ARP, VLANs, gateways, CIDR, longest-prefix match | Trace a local and a routed exchange, using a subnet reference card. | Explain why a remote destination uses the gateway's MAC; identify changes at routing boundaries. |
| DHCP, DNS, TCP/UDP, ports, TCP state, TLS visibility | Build a dependency chain and inspect selected packets. | Separate address configuration, naming, transport, and application success; identify what encryption hides. |
| MTU, MSS, ICMP, retransmission, troubleshooting | Diagnose the existing small-exchange/large-transfer failure. | Calculate a payload bound with stated assumptions; identify what the capture cannot establish. |
| Control/data planes, OSPF, BGP, ECMP, convergence | Work an OSPF failure timeline and a BGP policy comparison. | Distinguish route selection, forwarding-table installation, and observed service recovery. |
| VRFs versus VLANs; routes versus permission; NAT and return state | Compare the same endpoints across routing and policy contexts. | Explain why a route does not establish an authorized, working conversation. |
| Segmentation, DMZ/OT boundaries, management, redundancy, failure domains | Annotate the architecture and defend one improvement. | Identify a shared dependency and distinguish existing-session survival from new-session success. |
| WAN/cloud paths, firewalls, proxies, load balancers, monitoring | Compare component roles and check one cloud forward/return route. | Locate policy, translation, TLS termination, and visibility without inferring capabilities from diagram labels. |
| Telemetry, time, identity, incident scope, uncertainty, communication | Correlate staged evidence and give a handoff. | Separate observations from attack hypotheses, identify derived evidence, and recommend a proportionate action. |

Retain STP/LACP purpose, IPv6/Neighbor Discovery, HSRP/VRRP, VPNs/IPsec,
MPLS/SD-WAN, leaf/spine, underlays/overlays, VXLAN/EVPN, and ATT&CK vocabulary
as brief recognition prompts or references attached to the relevant challenge.
Recognition means explaining the purpose and one limitation, not operational
proficiency. No existing guide needs to be deleted.

Move protocol configuration, full BGP selection memorization, redistribution
design, EVPN route types, and advanced subnet arithmetic outside the required
day. Use the time gained for explanation and application of the core.

## One-Day Schedule

Complete existing prerequisite installation and readiness checks beforehand.
Advertise that setup time separately; it is outside the six teaching hours.
Reading all the guides is never prework.

| Time | Teaching minutes | Activity | Result |
| --- | ---: | --- | --- |
| 09:00–09:15 | 15 | Cold open: “The dashboard opens, but the transfer stalls.” Brief diagnostic, prediction, and one decoded observation. | Initial hypothesis and choice of next evidence. |
| 09:15–10:20 | 65 | Module 1: **Be the Packet** | Healthy path and dependency chain. |
| 10:20–10:35 | — | Break | |
| 10:35–11:20 | 45 | Module 1: **The Transfer That Stops** | Mechanism, calculation, and next test. |
| 11:20–12:00 | 40 | Module 1: **Pull One Link** | Before/during/after path explanation. |
| 12:00–12:30 | — | Lunch | |
| 12:30–13:30 | 60 | Module 2: **Spend Your Resilience Budget** | Annotated architecture and decision record. |
| 13:30–14:35 | 65 | Module 3: **Suspicious Is Not Proven** | Evidence ledger and qualified narrative. |
| 14:35–14:50 | — | Break | |
| 14:50–15:45 | 55 | Integrated capstone: **The Shift Handoff** | Revised artifacts and concise handoff. |
| 15:45–16:00 | 15 | Individual exit task, feedback, next-step references | Evidence of individual understanding. |
| **Total** | **360** | **Seven elapsed hours including breaks and lunch** | |

Target at least 210 minutes of student prediction, inspection, discussion, and
explanation. Avoid uninterrupted exposition longer than ten minutes. Verify
these facilitation targets during the pilot.

The opening diagnostic checks local versus remote destinations, DNS versus
connectivity, and what a successful TCP handshake establishes. Give novices
address cards, a small glossary, decoded examples, and a worked first hop.
Replace optional recognition tours with guided practice when needed; protect
the core challenges, capstone, and debrief. Do not quietly introduce a new
networking-experience prerequisite.

## Six Challenges

Use the existing enterprise/OT network as a fictional factory's operations
network. Reuse `ws-23`, `file-01`, and `historian-01`. Students keep approved
services available, understand a failure, then investigate suspicious behavior
while preserving essential operations.

Outage drills and the incident are separate episodes on the same network.
Do not imply that every timestamped fixture event caused the later incident.
Label new business requirements and hypothetical failures as scenario inputs.
All fixture paths below are relative to `labs/fixtures/`.

### 1. Be the Packet — 65 Minutes

**Play:** Give pairs endpoint, switch, router, and service cards. One learner
chooses the next step; the other asks which table or evidence justifies it.
Swap roles. Offer an equivalent text worksheet for solo and remote learners.

**Timing:** 10 minutes modeling, 30 tracing and inspecting, 15 changing one
condition, and 10 debriefing.

**Reuse:** `pcaps/foundations.pcap`, `network/dhcp.jsonl`,
`network/l2-control.json`, `routing/route-candidates.csv`, and the Layer 2 and
service-dependency exercises.

**Depth:** Record MAC addresses, IP addresses, VLAN, selected route, and return
behavior at relevant boundaries. Connect DHCP, DNS, TCP, and application
behavior, while explaining how caches and existing configuration can skip new
exchanges. Contrast the HTTP example with TLS visibility without revealing
the incident solution.

**Twist:** Remove the host route to `10.0.20.40` on a labeled paper variant.
Predict the winning prefix and eligible next hops. Trace the return direction
separately. A trunk capture shows one observation point; downstream header
changes remain predictions unless other evidence supports them.

**Checkpoint:** Each learner explains one routing boundary and one limitation.
Add the result to the packet-path sheet, without a separate report.

### 2. The Transfer That Stops — 45 Minutes

**Play:** Students choose between DNS, routing, transport, policy, and packet
size explanations before receiving the decisive evidence.

**Timing:** 5 minutes predicting, 20 investigating, 10 calculating and
challenging the diagnosis, and 10 debriefing.

**Reuse:** `pcaps/mtu-failure.pcap` and the troubleshooting bundle. Use a neutral
student-facing case label so its filename does not reveal the diagnosis;
retain a facilitator mapping to the original evidence.

**Depth:** Compare the completed handshake, oversized data, ICMP type 3/code 4
advertising MTU 1200, and retransmission. For IPv4 with 20-byte IP and TCP
headers and no options or encapsulation, calculate
`1200 - 20 - 20 = 1160` bytes of TCP payload. Distinguish this path constraint
from the advertised MSS. Additional headers reduce the data that fits; see
[RFC 6691](https://www.rfc-editor.org/rfc/rfc6691.html).

**Twist:** Choose evidence that would distinguish missing ICMP feedback from
a sender failing to act on it. ICMP visible at one capture point does not prove
delivery to the sender; this fixture also does not justify declaring ICMP
blocked everywhere. Use [RFC 1191](https://www.rfc-editor.org/rfc/rfc1191.html)
as the reference for the PMTU feedback mechanism.

**Checkpoint:** Cite decisive frames, reject one alternative, and request one
discriminating observation. Propose a repair and validation; do not change
the laptop's networking.

### 3. Pull One Link — 40 Minutes

**Play:** Freeze the network at link failure. Predict what the next packets
encounter before seeing the event sequence.

**Timing:** 5 minutes predicting, 15 reconstructing the timeline, 10 comparing
BGP choices, and 10 explaining the result.

**Reuse:** `routing/ospf.json`, `routing/bgp.json`,
`routing/route-events.jsonl`, and the convergence exercise.

**Depth:** Distinguish the LSA at 50 ms, forwarding-table update at 80 ms, and
flow rehash at 120 ms in this modeled trace. The installation time is neither
a measurement of application recovery nor a universal convergence time.
Compare OSPF cost with the fixture's BGP local-preference choice; inspect
accepted and rejected advertisements.

**Twist:** Compare a destination in a different VRF. Separate protocol decisions
that populate routes from longest-prefix lookup for a packet. Preference or
metric does not override a more-specific installed route; see
[RFC 1812, section 5.2.4.3](https://www.rfc-editor.org/rfc/rfc1812.html#section-5.2.4.3).

**Checkpoint:** Explain normal, transient, and converged behavior, including an
uncertainty about return traffic or middlebox state. Update the packet sheet.

### 4. Spend Your Resilience Budget — 60 Minutes

**Play:** Teams fund two improvements from a small menu of fictional effort
costs, protecting an explicit service requirement. Defend what remains
exposed. The costs are game constraints, not procurement estimates.

Start with two tokens and four one-token options: validate and repair firewall
state synchronization, add an independently routed backup path, add service
health monitoring, or provide independent management access. State which
failure each option addresses and its dependencies. Students may challenge an
option's value; no choice guarantees availability without supporting evidence.

**Timing:** 10 minutes on boundaries/components, 15 mapping flows and a cloud
return route, 20 choosing improvements and handling failure, and 15 defending
and revising the design.

**Reuse:** The six files under `architecture/`, plus `routing/vrfs.json`.

**Depth:** Compare the permitted server-to-historian and denied
workstation-to-historian paths. Mark routing, trust, management, failure, and
visibility boundaries. Compare stale firewall state synchronization with
20-percent WAN loss: device-up status does not establish service health. Check
a cloud forward and return route without equating attachment with reachability.

**Twist:** Reveal a shared dependency or stale state synchronization. Put any
extra condition on a scenario card. Distinguish established NAT sessions from
new connections. Request missing health measurements before recommending WAN
failover; a second link alone does not demonstrate service recovery.

**Checkpoint:** Produce an annotated diagram and a decision record covering
requirement, affected flow, improvement, residual risk, validation, and
rollback. Multiple designs can pass when their reasoning meets the constraints.

### 5. Suspicious Is Not Proven — 65 Minutes

**Play:** An alert arrives. Students decide how strongly to characterize the
activity and which evidence to request next.

**Timing:** 5 minutes briefing, three 12-minute investigation rounds, 14 minutes
building the narrative, and 10 debriefing.

**Reuse:** Existing incident sources, PCAP, ledger schema, and NetFlow/VRF
communication exercise. Release evidence in rounds:

1. Alert, asset context, and flows: write a provisional claim and rank the two
   most useful next sources.
2. DNS, endpoint, and authentication records: normalize selected timestamps,
   join identities, and revise confidence.
3. Firewall, proxy, and routing context: reconcile temporary egress permission
   with intended policy and evaluate the denied direct OT attempt.

Everyone receives the evidence needed to finish. Evidence requests prompt
discussion; hints carry no penalty. Delay the merged timeline and worked
narrative until students attempt their own ordering.

**Depth:** Correlate original and translated addresses. Distinguish successful
login from stolen credentials, periodicity from confirmed C2, and a denied
direct OT attempt from proof that all OT assets are unaffected. Mark Zeek
output derived from the PCAP and the SIEM's source events so they are not
counted as independent corroboration.

**Checkpoint:** Complete six to eight decisive rows of the existing ten-field
ledger. Give two plausible hypotheses, an attribution gap, and an action with
owner, operational effect, validation, and rollback. A qualified unresolved
conclusion can be the best answer.

### 6. The Shift Handoff — 55 Minutes

**Play:** A fresh variation arrives before the next team takes over. Students
apply their artifacts without a step-by-step guide.

**Timing:** 5 minutes briefing, 20 analysis, 10 preparing a handoff, 10 exchanging
and challenging handoffs, and 10 debriefing. Pairs exchange in parallel so
timing does not grow with class size.

**New material:** Author two deterministic case packets on the same network,
with one meaningful change per variant: for example, a missing return route or
a changed source routing context. Supply the route, policy, timing, and sensor
facts needed to reason about the change. Different addresses or shuffled
questions alone are insufficient. Keep each variant distinct from the original.

**Depth:** Trace the changed flow, explain a consequence for service or a
boundary, reconcile evidence, and recommend a next action. Rotate engineering,
architecture, security, and response viewpoints. Pairs cover two viewpoints
each; solo learners answer all four prompts.

**Checkpoint:** Deliver a two-minute handoff plus the three revised artifacts.
The recipient must identify the next check from the notes. In the final
15-minute exit block, use a different individual variation to check that team
fluency has not hidden a learner's misconception.

## Student Experience and Assessment

Maintain three deliverable bundles under `work/`: a packet-path sheet, an
architecture assessment, and an incident dossier containing the ledger,
narrative, and handoff. Intermediate notes feed those artifacts. A simple
checklist shows progress without 104 graded submissions.

Start with a modeled example, remove some prompts on the next attempt, and
finish with an independent variation. Keep worked answers available afterward.
Short retrieval questions with corrective feedback support this approach; see
CMU's [retrieval-practice guidance](https://www.cmu.edu/teaching/resources/instructionalstrategies/activelearningstrategies/retrievalpractice/index.html).

Use private predictions, pair discussion, and revised explanations. Welcome
changes of mind and give everyone a turn with the evidence. Avoid public speed
rankings, penalties for hints, forced acting, or rewards for the most dramatic
incident story.

Each brief needs a mission, time budget, prior knowledge, starting evidence,
deliverable, and success criteria. Offer three hints: where to look, which
field matters, then a worked step. Provide text tables alongside diagrams and
decoded excerpts alongside commands; keep raw evidence available.

Keep workbench scores as low-stakes practice. Use human or guided self-review
for the artifacts and capstone:

| Dimension | 0 — Needs revision | 1 — Developing | 2 — Demonstrated |
| --- | --- | --- | --- |
| Mechanism | Labels the symptom | Explains part of the path | Explains forwarding, policy/state, and relevant return or failure behavior |
| Evidence | Unsupported conclusion | Relevant source, weak linkage | Exact records support the claim; provenance is clear |
| Uncertainty | Treats assumptions as facts | Identifies a limitation | Gives an alternative and evidence that distinguishes it |
| Action and handoff | Vague or unjustified | Useful action, incomplete validation | Proportionate next step with owner, validation, and rollback where applicable |

Proposed completion threshold: at least 6/8 with no zero dimension after
feedback and revision, plus an individual explanation of the changed flow.
Accept multiple defensible design or containment decisions. Do not grade
open-ended judgment with exact-string matching.

## Implementation Priorities

Start with teachable briefs, evidence selections, templates, and facilitator
notes. Existing Markdown and terminal tools are sufficient. Pilot the learning
experience before adding navigation features. New paths below are proposed.

### Priority 0 — Define the Short Path

- [ ] Update `agenda.md` with the schedule, priorities, and rubric.
- [ ] Update root/module READMEs to distinguish the one-day route from the full
  reference library; make that distinction visible in navigation.
- [ ] Add `challenges/README.md`, six challenge briefs, and three artifact
  templates under `challenges/templates/`. Reuse the existing ledger schema.
- [ ] Add `facilitator/README.md` with timings, diagnostic interpretation,
  misconceptions, hint/reveal points, and sample graded responses.
- [ ] Replace repetitive assignments along the short path with shared artifact
  updates and topic-specific checkpoints.

Done when a facilitator can identify the day's route, outputs, and assessment
without reading all 104 guides.

### Priority 1 — Make the Evidence Support Every Task

- [ ] Map questions to observable facts or explicit hypothetical conditions;
  resolve gaps such as the VXLAN exercise.
- [ ] Prepare neutral student briefs and evidence selections with facilitator
  mappings to original files, records, and checksums.
- [ ] Separate predictions from outcomes and solutions as a teaching convention;
  no accounts, locks, or anti-cheating system.
- [ ] Author two capstone variants with defensible answer keys. Add only needed
  evidence to `labs/build_fixtures.py`, preserving reproducibility and distinct
  case versions; update the manifest and inventory when files are added.
- [ ] Ensure commands expose the evidence needed by the objective. MTU analysis,
  for example, needs packet/data lengths and retransmissions, not just MSS and
  ICMP fields.
- [ ] Document topology assumptions, capture locations, derived sources, and
  conclusions the evidence cannot establish.

Done when someone other than the author can solve each challenge from its
student materials without needing hidden facts.

### Priority 2 — Pilot, Then Improve Tooling Where Needed

- [ ] Run a timed pilot with beginners and experienced technical collaborators;
  include a solo learner using the self-review notes.
- [ ] Record time to first observation, setup/command friction, hints, missed
  concepts, artifact quality, and student feedback.
- [ ] If navigation is an obstacle, add a small challenge entry to `course.py`
  using the existing menu pattern; preserve current commands and guide access.
- [ ] Reuse workbench practice; add only missing convergence or changed-condition
  checks. Keep open-ended explanations outside exact-answer grading.
- [ ] Add targeted tests for changed commands, case consistency, and any new
  grading behavior. Avoid a generic scenario engine.

Done when the pilot fits six teaching hours and provides evidence about both
learning and enjoyment. Adjust timing and scope before adding more topics.

### Priority 3 — Optional Extensions

- [ ] Offer a loopback experiment as an alternative observation, with equivalent
  saved evidence available.
- [ ] Add take-home IPv6/ND, DNS caching, or WAN degradation challenges.
- [ ] Add VXLAN/EVPN packet and mapping evidence only if students need that
  extension. Give extensions separate time estimates and prerequisites.

Extensions are outside the six-hour requirement. Preserve the single-Mac,
local, open-source model: no required VM, container, cloud account, enterprise
equipment, or changes to laptop routing, firewall, or DNS configuration.

## Pilot Success Criteria and Validation

Use these as proposed targets, not proven outcomes:

- A prepared learner makes a meaningful prediction and observation within the
  first 15 minutes. Track installation problems separately.
- Instruction fits 360 minutes, including capstone and feedback, with at least
  210 minutes of active student work.
- At least 80% meet the rubric threshold after one revision. Record individual
  results alongside team results.
- Compare the individual exit task with the opening diagnostic using equivalent
  but different examples: changed path, cited evidence, and qualified claims.
- Median responses to “I wanted to find out what happened next” and “The
  challenge felt manageable” reach 4/5. Ask what dragged and what needed more
  explanation.
- Required work is completable offline after setup, including the solo route;
  privileged capture is never needed for the core outcomes.

If enjoyment is high but explanations stay shallow, improve checkpoints and
evidence prompts. If learning improves but the day overruns, shorten surveys
and repeated reporting. Protect investigation and debrief time.

Aligning objectives, activities, and assessment, and prioritizing what fits the
available time, follows CMU's
[teaching principles](https://www.cmu.edu/teaching/principles/teaching.html).
The games, schedule, and thresholds are proposals for this course and need
validation with its students.

When implementing, run fixture verification, workbench self-tests, existing
project tests, Markdown lint, and whitespace checks as relevant. Human
walkthroughs must check technical conclusions, missing evidence, premature
answer reveals, and consistency across case versions. Automated checks cannot
establish teachability or enjoyment.

## Completed Foundation from the Previous Plan

The previous navigation plan was marked implemented and verified. Preserve:

- [x] `./course` and compatible `python3 course.py` commands.
- [x] Numbered navigation, breadcrumbs, paging, and non-interactive output.
- [x] Short practice, input help, retry, and explicit answer reveal.
- [x] Fixture, workbench, navigation, and setup validation coverage.

Continue using dependency-free Python tooling. This curriculum does not need
a web app, third-party terminal interface, accounts, leaderboard, or persistent
progress system.
