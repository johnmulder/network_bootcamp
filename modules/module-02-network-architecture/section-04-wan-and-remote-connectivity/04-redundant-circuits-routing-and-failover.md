# Redundant Circuits, Routing, and Failover

> **Module 2 · Section 4**

## Why It Matters

WAN resilience depends on independent transport, usable route policy,
detection, capacity, and stateful-service continuity.

## Core Model

* Circuits from different providers may still share conduit, building entry,
  exchange, or upstream infrastructure.

* Route preference decides primary and backup use; ECMP or policy can use
  multiple circuits simultaneously.

* Failure detection must distinguish hard loss from high latency, loss, or
  partial reachability.

* Backup capacity must support critical traffic and preserve required security
  inspection.

* Failback can cause a second disruption, route oscillation, or state loss if
  not controlled.

## Reasoning Process

1. Map physical and provider diversity rather than counting circuits.

2. Document normal route preference and traffic distribution.

3. Model hard, soft, partial, and upstream failures.

4. Verify detection, convergence, capacity, policy symmetry, and failback.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-04-wan-and-remote-connectivity
   touch work/module-02-network-architecture/section-04-wan-and-remote-connectivity/04-redundant-circuits-routing-and-failover.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Redundant Circuits, Routing, and Failover** in
   `work/module-02-network-architecture/section-04-wan-and-remote-connectivity/04-redundant-circuits-routing-and-failover.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/wan.json
   jq '.circuits[] | {name, provider, state, loss_percent, capacity_mbps, preference}' labs/fixtures/architecture/wan.json
   jq '.routes, .sdwan_policy, .mpls' labs/fixtures/architecture/wan.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Redundant
   Circuits, Routing, and Failover**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `private-1` is preferred but degraded with 20 percent loss; `internet-vpn-1`
  is up, lower capacity, and encrypted.

* The branch default still points through HQ on the degraded private circuit,
  while the specific HQ prefix uses the VPN fixture.

* The MPLS service is provider-managed private routing but is explicitly not
  encrypted; SD-WAN policy chooses paths by application intent.

## Completion Standard

Submit
`work/module-02-network-architecture/section-04-wan-and-remote-connectivity/04-redundant-circuits-routing-and-failover.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. What hidden dependency can make two providers fail together?

2. Why is interface-up status an incomplete WAN health check?

3. What should be validated before automatic failback?
