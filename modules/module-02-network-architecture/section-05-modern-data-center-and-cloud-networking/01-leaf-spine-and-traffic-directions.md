# Leaf/Spine Architecture and Traffic Directions

> **Module 2 · Section 5**

## Why It Matters

Leaf/spine topologies provide predictable low-hop connectivity for data-center
east-west traffic while supporting north-south access through dedicated service
or border leaves.

## Core Model

* Endpoints connect to leaf switches; every leaf connects to every spine in the
  fabric.

* Spines provide transit between leaves and normally do not connect endpoints
  directly.

* East-west traffic moves between internal workloads; north-south traffic
  enters or leaves the data center.

* Equal-cost routed paths provide capacity and resilience without extending one
  Layer 2 tree through the core.

* Service insertion, border connectivity, and dual-homed endpoints can alter
  the simple two-tier path.

## Reasoning Process

1. Identify leaf, spine, border, service, and endpoint roles.

2. Trace same-leaf, cross-leaf, and north-south flows.

3. Enumerate ECMP paths and failure effects.

4. Locate routing, policy, service insertion, and observation points.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking
   touch work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/01-leaf-spine-and-traffic-directions.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Leaf/Spine Architecture and Traffic Directions** in
   `work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/01-leaf-spine-and-traffic-directions.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/cloud-routes.json
   jq '.attachments | to_entries[] | {attachment: .key, route_table: .value}' labs/fixtures/architecture/cloud-routes.json
   jq '.routes | to_entries[] | {table: .key, routes: .value}' labs/fixtures/architecture/cloud-routes.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Leaf/Spine
   Architecture and Traffic Directions**. Apply the numbered Reasoning Process
   in order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `corp-vpc` associates with `rt-corp`, which sends its default route through
  `security-vpc` and on-premises prefixes toward `on-prem`.

* `rt-security` targets `corp-vpc` for `10.20.0.0/16`. This is a modeled
  route, not proof of symmetric inspection or preserved state. The more
  specific on-premises route in `rt-corp` bypasses its security default.

* `rt-hybrid` has no default route, so attachment alone does not provide
  internet reachability.

## Completion Standard

Submit
`work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/01-leaf-spine-and-traffic-directions.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why does every leaf connect to every spine?

2. Where should an endpoint normally attach?

3. How can a required firewall make a nominally short east-west path longer?
