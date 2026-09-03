# Failure Domains, Redundancy, and Tradeoffs

> **Module 2 · Section 2**

## Why It Matters

Architecture must balance availability, scale, operability, cost, and
complexity. Redundancy helps only when failure modes are independent and
recovery is understandable.

## Core Model

* A failure domain is the set of services or components affected by one failure
  or change.

* Redundant elements can share hidden dependencies such as power, software,
  control plane, cabling, or upstream service.

* Complexity increases configuration combinations, testing burden, operational
  skill requirements, and recovery uncertainty.

* Availability requires detection, isolation, capacity, convergence, and
  validated procedures in addition to spare components.

* Blast radius and recovery confidence can matter more than maximizing
  theoretical redundancy.

## Reasoning Process

1. Name the service and enumerate components and dependencies on its critical
   path.

2. Group dependencies that can fail together.

3. Test whether surviving components have capacity and state to carry the
   service.

4. Compare the reliability benefit with added operational and failure
   complexity.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-02-enterprise-network-architecture
   touch work/module-02-network-architecture/section-02-enterprise-network-architecture/05-failure-domains-redundancy-and-tradeoffs.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Failure Domains, Redundancy, and Tradeoffs** in
   `work/module-02-network-architecture/section-02-enterprise-network-architecture/05-failure-domains-redundancy-and-tradeoffs.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   jq '.stp' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **Failure
   Domains, Redundancy, and Tradeoffs**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

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
`work/module-02-network-architecture/section-02-enterprise-network-architecture/05-failure-domains-redundancy-and-tradeoffs.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can two redundant devices belong to the same failure domain?

2. When does redundancy increase outage risk?

3. What evidence demonstrates that failover capacity is sufficient?
