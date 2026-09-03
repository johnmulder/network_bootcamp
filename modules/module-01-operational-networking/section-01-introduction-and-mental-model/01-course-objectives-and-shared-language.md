# Course Objectives and Shared Language

> **Module 1 · Section 1**

## Why It Matters

Network work crosses engineering, architecture, security, and incident
response. A shared vocabulary prevents each discipline from describing the same
packet path with incompatible assumptions.

## Core Model

* Operational fluency means being able to explain a path, identify the deciding
  device or table, and state what evidence supports the explanation.

* Architecture describes intended structure and constraints; engineering
  operates that structure; security defines and enforces acceptable behavior;
  incident response reconstructs observed behavior.

* A useful explanation names endpoints, addresses, protocols, direction,
  boundaries, state, and evidence instead of saying only that a connection
  works or fails.

* Terms should be tied to observable behavior. For example, a route is an entry
  used for forwarding, while a session is state maintained by endpoints or
  middleboxes.

* The course values defensible reasoning over memorizing vendor commands.

## Reasoning Process

1. State the behavior being explained in one sentence, including source,
   destination, protocol, and direction.

2. Name the relevant layers and boundaries without assuming a device performs a
   function merely because it appears on a diagram.

3. Separate configuration facts, observed evidence, and working assumptions.

4. Translate the conclusion into language that each participating discipline
   can verify.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-01-introduction-and-mental-model
   touch work/module-01-operational-networking/section-01-introduction-and-mental-model/01-course-objectives-and-shared-language.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Course Objectives and Shared Language** in
   `work/module-01-operational-networking/section-01-introduction-and-mental-model/01-course-objectives-and-shared-language.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   sed -n '1,120p' labs/fixtures/architecture/enterprise.md
   python3 -m json.tool labs/fixtures/manifest.json | sed -n '1,80p'
   ```

4. In the output file, add a `## Analysis` section for **Course Objectives and
   Shared Language**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The manifest reports the case name `network-bootcamp-reference` and 29
  checksum-protected fixture files.

* The architecture places `ws-23` at `10.0.10.23`, `file-01` at `10.0.20.40`,
  and the OT networks behind two explicit firewall boundaries.

* Your explanation identifies path, policy, state, and evidence as separate
  questions rather than treating the diagram as proof of live behavior.

## Completion Standard

Submit
`work/module-01-operational-networking/section-01-introduction-and-mental-model/01-course-objectives-and-shared-language.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Can you distinguish an architecture claim from an observation about live
   traffic?

2. What details are missing from the statement, “The firewall blocked it”?

3. How would a network engineer and an incident responder describe the same
   failed connection differently?
