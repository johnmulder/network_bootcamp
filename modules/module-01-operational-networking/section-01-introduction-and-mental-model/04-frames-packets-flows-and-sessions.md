# Frames, Packets, Flows, and Sessions

> **Module 1 · Section 1**

## Why It Matters

These terms describe different views of communication. Correctly choosing the
unit of analysis prevents errors such as treating a Layer 2 destination as an
end-to-end destination.

## Core Model

* A frame is a link-local delivery unit with Layer 2 source and destination
  addresses. It is normally replaced at each routed hop.

* An IP packet carries end-to-end network-layer addresses, although NAT can
  rewrite them at a boundary.

* A transport segment or datagram carries ports and protocol state used by
  applications.

* A flow is an analytical grouping, commonly identified by source and
  destination addresses, ports, and transport protocol.

* A session is maintained state. Its definition depends on the endpoint,
  firewall, proxy, VPN, or monitoring tool observing it.

## Reasoning Process

1. Select one captured communication and identify its frame, packet, transport,
   flow, and session representations.

2. Mark which identifiers remain stable across a routed boundary and which can
   change.

3. Identify every component that may create independent session state.

4. State which representation is required to answer the current question.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-01-introduction-and-mental-model
   touch work/module-01-operational-networking/section-01-introduction-and-mental-model/04-frames-packets-flows-and-sessions.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Frames, Packets, Flows, and Sessions** in
   `work/module-01-operational-networking/section-01-introduction-and-mental-model/04-frames-packets-flows-and-sessions.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   sed -n '1,120p' labs/fixtures/architecture/enterprise.md
   python3 -m json.tool labs/fixtures/manifest.json | sed -n '1,80p'
   ```

4. In the output file, add a `## Analysis` section for **Frames, Packets, Flows,
   and Sessions**. Apply the numbered Reasoning Process in order. For each step,
   cite at least one exact command result and label the statement as an
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
`work/module-01-operational-networking/section-01-introduction-and-mental-model/04-frames-packets-flows-and-sessions.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why is the destination MAC address usually not the remote server's MAC
   address?

2. Can two tools report different session counts for the same traffic without
   either being wrong?

3. Which fields normally define a five-tuple flow?
