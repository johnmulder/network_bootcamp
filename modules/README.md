# Course Modules

These modules turn the [course agenda](../agenda.md) into exact teaching and
practice instructions. Everything runs on one Mac using the open-source tools
described in the [prerequisites](../prerequisites/README.md).

The [104-guide evidence matrix](evidence-matrix.md) maps each topic to its
prediction, demonstration, exact source, and completion criterion. Practical
guides use focused local commands. FHRP, collapsed-core, leaf/spine, and
VXLAN/EVPN exercises state conceptual assumptions where device evidence is
absent. No exercise requires inventing a table, packet, or measurement.

## One-Day Route and Extended Study

Start with the [six-hour challenge path](../challenges/README.md). It draws on
these modules but requires only three shared deliverables. The guide-level
submission instructions below are optional extended-study exercises. During
the one-day course, consult a guide after attempting its challenge because
reference guides include worked observations.

## Current Reference Curriculum

| Module | Sections | Guides | Workbench | Outcome |
| --- | ---: | ---: | --- | --- |
| [1 — Operational Networking](module-01-operational-networking/README.md) | 8 | 43 | [6 activities, 25 questions](module-01-operational-networking/workbench/README.md) | Explain and validate an end-to-end packet path |
| [2 — Network Architecture](module-02-network-architecture/README.md) | 8 | 29 | [5 activities, 30 questions](module-02-network-architecture/workbench/README.md) | Assess boundaries, dependencies, and failure behavior |
| [3 — Incident Response and Integration](module-03-incident-response-and-integration/README.md) | 7 | 32 | [5 activities, 28 questions](module-03-incident-response-and-integration/workbench/README.md) | Build a qualified incident assessment and handoff |

For extended study, start with Module 1 unless you can already complete its
packet-path review.
Each module's final artifact becomes useful context for the next:

1. Module 1 produces an evidence-backed packet-path review.
2. Module 2 adds an annotated architecture and failure assessment.
3. Module 3 turns path and architecture knowledge into an evidence ledger,
   incident narrative, and cross-functional handoff.

## Learning Workflow

For optional extended study with saved evidence, use this sequence for a
selected subsection. Conceptual references provide their own self-checks.

Run `./course verify` once at the start. Keep notes in the existing packet,
architecture, or incident artifact, or create a Markdown file under `work/`
mirroring the selected guide's path. There is no need to repeat setup or
copy every command output for every guide. A few decisive citations are
more useful than an unannotated transcript. Read worked reasoning after
predicting; opening worked reference answers can expose a related assessment.

1. **Orient:** Read the guide's objective, mental model, and named fixture
   paths before running commands.
2. **Predict:** Write the expected path, state, policy decision, or evidence
   before inspecting the fixture.
3. **Observe:** Run the exact commands from the repository root and preserve
   the relevant output under the guide's `work/` path.
4. **Explain:** Connect each observation to the networking, architecture, or
   investigation rule that makes it meaningful.
5. **Challenge:** State what the evidence does not prove and identify the next
   evidence that would reduce uncertainty.
6. **Practice:** Use the linked workbench activity for scored, repeatable
   questions and immediate feedback.
7. **Complete:** Produce the requested artifact and test it against the guide's
   completion standard.

The workbench score checks exact facts. The written artifact checks the harder
skill: making a defensible claim, citing the evidence that supports it, and
preserving the limitations of that evidence.

## Suggested Study Routes

These optional estimates need learner validation; they add no required time.

| Need | Prerequisite | Route | Suggested time |
| --- | --- | --- | --- |
| Foundations | Read one TShark row using Challenge 1 | Module 1 addressing → ARP → inter-VLAN → route selection → DNS contrasts | 60–90 minutes |
| Architecture | Explain both directions of a routed exchange | Module 2 foundation check → flows → firewall/NAT → cloud → failure domains | 60–90 minutes |
| Incident reasoning | Separate path, policy, and state | Module 3 packet/flow evidence → endpoint/SIEM → visibility gaps → ledger → handoff | 60–90 minutes |
| Modern transport | TCP and TLS boundaries | Public TLS exemplar → QUIC exemplar → saved performance comparison | 45–50 minutes |

Use the directory order below for a longer course. The concise routes select
related guides; they do not require completing all 104 in one day.

## Workbench Entry Points

Run every command from the repository root:

```sh
python3 modules/module-01-operational-networking/workbench/module1_workbench.py list
python3 modules/module-02-network-architecture/workbench/module2_workbench.py list
python3 modules/module-03-incident-response-and-integration/workbench/module3_workbench.py list
```

Each workbench supports `demo`, focused `run` activities, mixed review, seeded
question order, and `self-test`. Module 3 also builds a normalized incident
timeline. See the workbench README linked in the curriculum table for the full
command set and facilitation pattern.

## Completion Standard

A module is complete when the learner can:

- reproduce the relevant observation from the named fixture;
- distinguish recorded fact from interpretation, assumption, and unknown;
- explain both the forward path and the important return or failure path;
- name an evidence limitation and an efficient next check; and
- deliver the module artifact so another role can review or continue the work.
