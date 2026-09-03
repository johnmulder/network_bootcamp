# Course Modules

These modules turn the [course agenda](../agenda.md) into exact teaching and
practice instructions. Everything runs on one Mac using the open-source tools
described in the [prerequisites](../prerequisites/README.md).

Each subsection guide names its evidence, provides runnable commands, explains
the expected observations, assigns a unique submission path under `work/`, and
defines completion. The [local lab dataset](../labs/README.md) supplies the
shared evidence, and each module includes a Python workbench for immediate
feedback.

## Current Curriculum

| Module | Sections | Guides | Workbench | Outcome |
| --- | ---: | ---: | --- | --- |
| [1 — Operational Networking](module-01-operational-networking/README.md) | 8 | 43 | [5 activities, 21 questions](module-01-operational-networking/workbench/README.md) | Explain and validate an end-to-end packet path |
| [2 — Network Architecture](module-02-network-architecture/README.md) | 8 | 29 | [5 activities, 30 questions](module-02-network-architecture/workbench/README.md) | Assess boundaries, dependencies, and failure behavior |
| [3 — Incident Response and Integration](module-03-incident-response-and-integration/README.md) | 7 | 32 | [5 activities, 28 questions](module-03-incident-response-and-integration/workbench/README.md) | Build a qualified incident assessment and handoff |

Start with Module 1 unless you can already complete its packet-path review.
Each module's final artifact becomes useful context for the next:

1. Module 1 produces an evidence-backed packet-path review.
2. Module 2 adds an annotated architecture and failure assessment.
3. Module 3 turns path and architecture knowledge into an evidence ledger,
   incident narrative, and cross-functional handoff.

## Learning Workflow

Use this sequence for every subsection:

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
