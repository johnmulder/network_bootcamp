# High Availability: Active/Active and Active/Passive

> **Module 2 · Section 2**

## Why It Matters

High availability is a service property created by redundant components, state,
health detection, and recovery behavior. Device count alone does not establish
availability.

## Core Model

* Active/passive designs keep one node serving while another waits to assume
  responsibility.

* Active/active designs serve traffic on multiple nodes, but may divide flows,
  partitions, or functions rather than duplicate every operation.

* Health checks must detect service failure, not only device power or interface
  state.

* Stateful services require session, NAT, identity, or application state to be
  synchronized or safely re-created.

* Split-brain, stale state, dependency failure, and shared infrastructure can
  defeat nominal redundancy.

## Reasoning Process

1. Define the service and its acceptable interruption, loss, and recovery
   behavior.

2. Map active responsibilities, shared state, and health signals.

3. Fail each component and dependency separately, including partial failures.

4. Verify that recovery restores both directions and does not create duplicate
   ownership.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-02-enterprise-network-architecture
   touch work/module-02-network-architecture/section-02-enterprise-network-architecture/04-high-availability-active-active-and-active-passive.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **High
   Availability: Active/Active and Active/Passive** in
   `work/module-02-network-architecture/section-02-enterprise-network-architecture/04-high-availability-active-active-and-active-passive.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   jq '.stp' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **High
   Availability: Active/Active and Active/Passive**. Apply the numbered
   Reasoning Process in order. Tie every design or failure claim to a named
   component, boundary, route, policy, or fixture field.

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
`work/module-02-network-architecture/section-02-enterprise-network-architecture/04-high-availability-active-active-and-active-passive.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why is active/active not automatically more available?

2. What makes a health check meaningful?

3. Which shared component can remain a single point of failure?
