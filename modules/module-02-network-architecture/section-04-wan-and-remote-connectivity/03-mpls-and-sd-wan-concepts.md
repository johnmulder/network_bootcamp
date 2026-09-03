# MPLS and SD-WAN Concepts

> **Module 2 · Section 4**

## Why It Matters

MPLS and SD-WAN are broad solution families. The useful conceptual distinction
is between provided transport, overlay control, path selection, and security
responsibility.

## Core Model

* An MPLS VPN can provide provider-managed private reachability but does not
  inherently encrypt customer traffic.

* Labels guide forwarding inside the provider network while customer routes
  define VPN reachability.

* SD-WAN commonly builds overlays across one or more transports and applies
  centralized policy to path selection.

* Application-aware steering depends on classification, link measurement,
  controller state, and edge enforcement.

* Internet, broadband, cellular, and private circuits can share an overlay
  while retaining different failure and trust properties.

## Reasoning Process

1. Identify underlay transports and who operates each one.

2. Identify overlay endpoints, route distribution, policy control, and
   encryption.

3. Trace how one application selects and changes paths.

4. Evaluate controller loss, edge failure, degraded links, and provider
   isolation.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-04-wan-and-remote-connectivity
   touch work/module-02-network-architecture/section-04-wan-and-remote-connectivity/03-mpls-and-sd-wan-concepts.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **MPLS
   and SD-WAN Concepts** in
   `work/module-02-network-architecture/section-04-wan-and-remote-connectivity/03-mpls-and-sd-wan-concepts.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/wan.json
   jq '.circuits[] | {name, provider, state, loss_percent, capacity_mbps, preference}' labs/fixtures/architecture/wan.json
   jq '.routes, .sdwan_policy, .mpls' labs/fixtures/architecture/wan.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **MPLS and
   SD-WAN Concepts**. Apply the numbered Reasoning Process in order. Tie every
   design or failure claim to a named component, boundary, route, policy, or
   fixture field.

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
`work/module-02-network-architecture/section-04-wan-and-remote-connectivity/03-mpls-and-sd-wan-concepts.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Does MPLS imply encryption?

2. What information must an SD-WAN edge use to steer an application?

3. Which functions remain when the central controller is unreachable?
