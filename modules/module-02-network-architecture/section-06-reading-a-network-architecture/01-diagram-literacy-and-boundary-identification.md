# Diagram Literacy and Boundary Identification

> **Module 2 · Section 6**

## Why It Matters

Architecture diagrams compress many kinds of relationships into shapes and
lines. Effective reading starts by decoding notation and marking what the
diagram omits.

## Core Model

* A line may represent physical connection, logical adjacency, tunnel, route
  exchange, permitted flow, or dependency.

* Layer 2, Layer 3, trust, security, failure, management, and visibility
  boundaries are related but not interchangeable.

* Icons suggest functions but do not prove routing, policy, state, translation,
  or termination behavior.

* Redundancy must be evaluated end to end, including shared dependencies.

* Diagram title, scope, version, owner, and source affect how much confidence
  it deserves.

## Reasoning Process

1. Read legend, scope, date, assumptions, and abstraction level.

2. Inventory components and classify every relationship.

3. Mark each boundary type with a distinct notation.

4. Create a questions list for missing addressing, routing, policy, state,
   ownership, and evidence.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-06-reading-a-network-architecture
   touch work/module-02-network-architecture/section-06-reading-a-network-architecture/01-diagram-literacy-and-boundary-identification.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Diagram Literacy and Boundary Identification** in
   `work/module-02-network-architecture/section-06-reading-a-network-architecture/01-diagram-literacy-and-boundary-identification.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/architecture/components.json
   jq '.' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Diagram
   Literacy and Boundary Identification**. Apply the numbered Reasoning Process
   in order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The diagram establishes named zones and relationships but relies on the flow
  table and VRF file for policy and route facts.

* Flow `F3` is the only listed enterprise-to-OT application flow allowed
  directly; flow `F4` is denied.

* The management path uses a distinct VRF and `jump-host-policy`, which must be
  shown as a management and trust boundary.

## Completion Standard

Submit
`work/module-02-network-architecture/section-06-reading-a-network-architecture/01-diagram-literacy-and-boundary-identification.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. What does a firewall icon prove by itself?

2. Can one link cross several boundary types?

3. Which metadata determines whether a diagram is authoritative?
