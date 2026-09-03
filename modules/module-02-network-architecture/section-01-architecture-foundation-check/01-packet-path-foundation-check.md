# Packet-Path Foundation Check

> **Module 2 · Section 1**

## Why It Matters

Architecture analysis begins with packet behavior. This foundation check
confirms that a participant can turn a diagram into forward and return paths
without inventing missing details.

## Core Model

* A line on a diagram shows an intended relationship, not necessarily Layer 2
  adjacency, Layer 3 reachability, policy permission, or current health.

* Every flow requires endpoint configuration, a forwarding path, a return path,
  applicable policy, and any state created by middleboxes.

* Architecture decisions should be evaluated against requirements and failure
  behavior rather than visual symmetry.

* Unknown routing contexts, address translation, encryption, ownership, or
  telemetry must be recorded explicitly.

* The same reference flow will be reused throughout the module to compare
  design choices.

## Reasoning Process

1. Select a source, destination, protocol, direction, and success criterion.

2. Trace Layer 2 and Layer 3 transitions using only the facts provided.

3. Mark routing, policy, state, trust, failure, and visibility boundaries.

4. List unresolved questions before evaluating whether the design is good.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-01-architecture-foundation-check
   touch work/module-02-network-architecture/section-01-architecture-foundation-check/01-packet-path-foundation-check.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Packet-Path Foundation Check** in
   `work/module-02-network-architecture/section-01-architecture-foundation-check/01-packet-path-foundation-check.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq 'to_entries[] | {vrf: .key, routes: .value}' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Architecture Analysis` section for
   **Packet-Path Foundation Check**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The reference flow `F1` begins at `ws-23` in VLAN 10 and reaches `file-01` in
  VLAN 20 through a Layer 3 and policy decision.

* The CORP routing context contains both endpoint prefixes and a default route;
  the OT context does not.

* The diagram does not prove current route installation, policy state, return
  path, or sensor health, so those remain explicit unknowns.

## Completion Standard

Submit
`work/module-02-network-architecture/section-01-architecture-foundation-check/01-packet-path-foundation-check.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Which parts of your path are confirmed and which are inferred?

2. Did you independently establish the return path?

3. What missing fact would most change your architecture assessment?
