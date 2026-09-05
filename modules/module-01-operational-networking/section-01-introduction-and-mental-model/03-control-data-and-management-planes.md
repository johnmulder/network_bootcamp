# Control, Data, and Management Planes

> **Module 1 · Section 1**

## Why It Matters

The three-plane model separates how forwarding knowledge is learned, how
packets are moved, and how operators observe or change a device. It is
essential for explaining partial failures.

## Core Model

* The control plane exchanges or calculates information used to build
  forwarding state, such as routes, neighbors, and spanning-tree decisions.

* The data plane applies installed forwarding state to packets at operational
  speed.

* The management plane exposes configuration, telemetry, authentication,
  software lifecycle, and administrative access.

* A control-plane failure may leave stale data-plane state temporarily working.
  A management-plane failure may prevent access while forwarding continues.

* Policies can affect more than one plane, so an investigation must identify
  which plane produced or enforced a decision.

## Reasoning Process

1. Name the observed symptom and determine whether forwarding, learning, or
   administration is affected.

2. Identify the relevant state in each plane: learned information, installed
   forwarding entry, and management evidence.

3. Check whether the planes agree or whether one contains stale, missing, or
   inaccessible state.

4. Predict what should persist and what should converge after a failure.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-01-introduction-and-mental-model
   touch work/module-01-operational-networking/section-01-introduction-and-mental-model/03-control-data-and-management-planes.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Control, Data, and Management Planes** in
   `work/module-01-operational-networking/section-01-introduction-and-mental-model/03-control-data-and-management-planes.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   sed -n '1,120p' labs/fixtures/architecture/enterprise.md
   python3 -m json.tool labs/fixtures/manifest.json | sed -n '1,80p'
   ```

4. In the output file, add a `## Analysis` section for **Control, Data, and
   Management Planes**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The manifest reports the case name `network-bootcamp-reference` and 36
  checksum-protected fixture files.

* The architecture places `ws-23` at `10.0.10.23`, `file-01` at `10.0.20.40`,
  and the OT networks behind two explicit firewall boundaries.

* Your explanation identifies path, policy, state, and evidence as separate
  questions rather than treating the diagram as proof of live behavior.

## Completion Standard

Submit
`work/module-01-operational-networking/section-01-introduction-and-mental-model/03-control-data-and-management-planes.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Can the data plane continue when the control plane is unavailable?

2. Why does successful management access not prove application forwarding
   works?

3. Which plane would explain a correct route that was never installed for
   forwarding?
