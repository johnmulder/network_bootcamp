# Access, Distribution, Core, and Collapsed Core

> **Module 2 · Section 2**

## Why It Matters

Hierarchical campus design assigns distinct responsibilities to access,
distribution, and core layers. The hierarchy is a reasoning model, not a
requirement that each role use separate hardware.

## Core Model

* The access layer connects endpoints and often supplies edge security, VLAN
  membership, power, and first-line telemetry.

* The distribution layer aggregates access, provides Layer 3 boundaries,
  applies policy, and contains failures.

* The core provides resilient high-speed transport between major blocks and
  should avoid unnecessary state or complexity.

* A collapsed core combines distribution and core roles when scale or topology
  does not justify a separate tier.

* Physical devices, logical roles, and administrative ownership may not align
  one-to-one.

## Reasoning Process

1. Identify endpoint attachment, aggregation, and transit functions on the
   diagram.

2. Assign logical roles based on behavior rather than device labels.

3. Locate routing, policy, redundancy, and management responsibilities.

4. Test whether the hierarchy contains failures and supports required growth.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-02-enterprise-network-architecture
   touch work/module-02-network-architecture/section-02-enterprise-network-architecture/01-access-distribution-core-and-collapsed-core.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Access, Distribution, Core, and Collapsed Core** in
   `work/module-02-network-architecture/section-02-enterprise-network-architecture/01-access-distribution-core-and-collapsed-core.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   jq '.stp' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **Access,
   Distribution, Core, and Collapsed Core**. Apply the numbered Reasoning
   Process in order. Tie every design or failure claim to a named component,
   boundary, route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The reference architecture separates user, server, management, OT DMZ, and
  supervisory roles rather than representing one flat failure domain.

* `sw-dist-1` is the modeled spanning-tree root and one access-to-access path
  is non-forwarding.

* The failure data distinguishes endpoint isolation, stale firewall session
  synchronization, degraded WAN transport, and a stale DNS answer.

## Completion Standard

Submit
`work/module-02-network-architecture/section-02-enterprise-network-architecture/01-access-distribution-core-and-collapsed-core.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can one device perform both distribution and core roles?

2. Why should a core generally avoid unnecessary service state?

3. What requirement would justify adding a distinct distribution layer?
