# Transit Gateways and Hybrid Connectivity

> **Module 2 · Section 5**

## Why It Matters

Transit constructs connect many virtual networks and on-premises sites through
centralized route exchange and policy. Scale improves, but route propagation
and blast radius become critical.

## Core Model

* A transit gateway or hub centralizes attachments and route tables for
  multiple networks.

* Attachments can associate with one route table and propagate routes to others
  under explicit policy.

* Peering, VPN, dedicated circuits, and SD-WAN can provide hybrid underlay
  paths.

* Overlapping prefixes, asymmetric propagation, summarization, and default
  routes can produce unexpected reachability.

* Central inspection requires symmetric service insertion and careful handling
  of state and return routes.

## Reasoning Process

1. Map every attachment to its associated and propagated route tables.

2. Resolve the forward and return path one transit decision at a time.

3. Check prefix overlap, route preference, default propagation, and inspection
   insertion.

4. Model attachment, circuit, route, and centralized-service failures.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking
   touch work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/04-transit-gateways-and-hybrid-connectivity.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Transit Gateways and Hybrid Connectivity** in
   `work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/04-transit-gateways-and-hybrid-connectivity.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/cloud-routes.json
   jq '.attachments | to_entries[] | {attachment: .key, route_table: .value}' labs/fixtures/architecture/cloud-routes.json
   jq '.routes | to_entries[] | {table: .key, routes: .value}' labs/fixtures/architecture/cloud-routes.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Transit
   Gateways and Hybrid Connectivity**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

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
`work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/04-transit-gateways-and-hybrid-connectivity.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can two attached networks still lack mutual reachability?

2. How can centralized inspection create asymmetric routing?

3. What is the blast radius of an incorrect propagated default route?
