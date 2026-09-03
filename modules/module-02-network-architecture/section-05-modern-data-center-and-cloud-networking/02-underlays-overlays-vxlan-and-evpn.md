# Underlays, Overlays, VXLAN, and EVPN

> **Module 2 · Section 5**

## Why It Matters

Modern fabrics separate IP transport from logical tenant or segment
reachability. The underlay carries tunnels; the overlay identifies and
distributes virtual networks.

## Core Model

* The underlay provides IP reachability between tunnel endpoints, usually with
  a simple routed fabric.

* VXLAN encapsulates Layer 2 or Layer 3 traffic in UDP and uses a VNI to
  identify a logical segment.

* Tunnel endpoints add and remove VXLAN headers at the fabric edge.

* EVPN distributes MAC, IP, and reachability information through BGP
  control-plane routes.

* Troubleshooting must prove both underlay reachability and overlay mapping,
  then account for encapsulation MTU.

## Reasoning Process

1. Identify original endpoints, VNI, tunnel endpoints, and underlay addresses.

2. Verify the underlay route between tunnel endpoints.

3. Verify the overlay control-plane mapping for the destination.

4. Trace encapsulation, transport, decapsulation, and return behavior.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking
   touch work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Underlays, Overlays, VXLAN, and EVPN** in
   `work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/cloud-routes.json
   jq '.attachments | to_entries[] | {attachment: .key, route_table: .value}' labs/fixtures/architecture/cloud-routes.json
   jq '.routes | to_entries[] | {table: .key, routes: .value}' labs/fixtures/architecture/cloud-routes.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Underlays,
   Overlays, VXLAN, and EVPN**. Apply the numbered Reasoning Process in order.
   Tie every design or failure claim to a named component, boundary, route,
   policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `corp-vpc` associates with `rt-corp`, which sends its default route through
  `security-vpc` and on-premises prefixes toward `on-prem`.

* `rt-security` returns `10.20.0.0/16` to `corp-vpc`, supporting a symmetric
  centralized-inspection path for that prefix.

* `rt-hybrid` has no default route, so attachment alone does not provide
  internet reachability.

## Completion Standard

Submit
`work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can a healthy underlay coexist with a broken overlay?

2. What does a VNI identify?

3. Why does VXLAN create a new MTU consideration?
