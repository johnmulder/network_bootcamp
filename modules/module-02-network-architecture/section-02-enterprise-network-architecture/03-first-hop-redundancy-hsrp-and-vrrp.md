# First-Hop Redundancy, HSRP, and VRRP

> **Module 2 · Section 2**

## Why It Matters

First-hop redundancy allows hosts to use a stable default-gateway address while
multiple routers can provide forwarding.

## Core Model

* A virtual IP address and virtual MAC represent the default gateway presented
  to hosts.

* One device normally owns active forwarding responsibility for a group while a
  peer is prepared to take over.

* HSRP and VRRP differ in details but provide the same conceptual service:
  resilient first-hop ownership.

* Priority, preemption, object tracking, timers, and interface state influence
  which device becomes active.

* Gateway redundancy does not guarantee upstream routing, policy, or
  stateful-service redundancy.

## Reasoning Process

1. Identify the virtual gateway, physical peers, active owner, and tracked
   dependencies.

2. Trace normal traffic through the active device and verify the return path.

3. Fail the active device or tracked uplink and order ownership,
   neighbor-cache, and routing changes.

4. Check for state, policy, or asymmetric-path effects after takeover.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-02-enterprise-network-architecture
   touch work/module-02-network-architecture/section-02-enterprise-network-architecture/03-first-hop-redundancy-hsrp-and-vrrp.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **First-Hop Redundancy, HSRP, and VRRP** in
   `work/module-02-network-architecture/section-02-enterprise-network-architecture/03-first-hop-redundancy-hsrp-and-vrrp.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   jq '.stp' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **First-Hop
   Redundancy, HSRP, and VRRP**. Apply the numbered Reasoning Process in order.
   Tie every design or failure claim to a named component, boundary, route,
   policy, or fixture field.

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
`work/module-02-network-architecture/section-02-enterprise-network-architecture/03-first-hop-redundancy-hsrp-and-vrrp.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a virtual gateway remain reachable while upstream connectivity is
   broken?

2. What does preemption change?

3. Which endpoint cache may need to learn a new gateway MAC after failover?
