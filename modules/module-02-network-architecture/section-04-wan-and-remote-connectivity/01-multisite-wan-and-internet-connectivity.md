# Multisite WAN and Internet Connectivity

> **Module 2 · Section 4**

## Why It Matters

A WAN connects sites across external transport with different latency,
capacity, ownership, and failure characteristics than a campus LAN.

## Core Model

* Underlay circuits provide physical or provider transport; routing determines
  usable reachability over them.

* Sites need address plans, route exchange, security boundaries, shared
  services, and failure behavior.

* Internet connectivity can be centralized, distributed, or hybrid, changing
  egress, return paths, inspection, and identity.

* Provider handoffs and service-level objectives do not remove customer-side
  routing or capacity dependencies.

* DNS, authentication, cloud services, and management traffic can make a branch
  dependent on remote sites.

## Reasoning Process

1. Identify site requirements, critical flows, latency, capacity, and external
   dependencies.

2. Map circuits, provider boundaries, routing exchanges, and internet exits.

3. Trace forward and return paths for intersite and internet traffic.

4. Fail each circuit or hub and evaluate surviving capacity, policy, and shared
   services.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-04-wan-and-remote-connectivity
   touch work/module-02-network-architecture/section-04-wan-and-remote-connectivity/01-multisite-wan-and-internet-connectivity.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Multisite WAN and Internet Connectivity** in
   `work/module-02-network-architecture/section-04-wan-and-remote-connectivity/01-multisite-wan-and-internet-connectivity.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/wan.json
   jq '.circuits[] | {name, provider, state, loss_percent, capacity_mbps, preference}' labs/fixtures/architecture/wan.json
   jq '.routes, .sdwan_policy, .mpls' labs/fixtures/architecture/wan.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Multisite
   WAN and Internet Connectivity**. Apply the numbered Reasoning Process in
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
`work/module-02-network-architecture/section-04-wan-and-remote-connectivity/01-multisite-wan-and-internet-connectivity.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. How does internet-exit placement affect inspection and return routing?

2. What branch services fail when the WAN is down?

3. Why does a second circuit not guarantee independent transport?
