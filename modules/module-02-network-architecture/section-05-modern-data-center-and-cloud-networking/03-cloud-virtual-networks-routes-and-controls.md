# Cloud Virtual Networks, Routes, and Controls

> **Module 2 · Section 5**

## Why It Matters

Cloud networks expose logical constructs through provider control planes. The
packet model still applies, but diagrams must include implicit routers,
distributed controls, and platform-owned dependencies.

## Core Model

* A virtual network contains address ranges, subnets, virtual interfaces, route
  tables, and gateways implemented by the provider.

* Subnet labels do not necessarily imply Layer 2 broadcast behavior like a
  physical VLAN.

* Route tables determine next targets such as local delivery, internet, NAT,
  firewall, peering, or transit.

* Security groups are commonly stateful interface-level controls; network ACLs
  are commonly stateless subnet-level controls, though semantics vary by
  provider.

* Public addresses, managed load balancers, private endpoints, and service
  networking create multiple identity and observation layers.

## Reasoning Process

1. Inventory virtual interfaces, addresses, subnets, route associations, and
   gateway targets.

2. Trace the effective route and every distributed or centralized policy.

3. Mark provider-managed translation, load balancing, and service endpoints.

4. Identify telemetry sources and facts the customer cannot directly observe.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking
   touch work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/03-cloud-virtual-networks-routes-and-controls.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Cloud
   Virtual Networks, Routes, and Controls** in
   `work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/03-cloud-virtual-networks-routes-and-controls.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/architecture/cloud-routes.json
   jq '.attachments | to_entries[] | {attachment: .key, route_table: .value}' labs/fixtures/architecture/cloud-routes.json
   jq '.routes | to_entries[] | {table: .key, routes: .value}' labs/fixtures/architecture/cloud-routes.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Cloud
   Virtual Networks, Routes, and Controls**. Apply the numbered Reasoning
   Process in order. Tie every design or failure claim to a named component,
   boundary, route, policy, or fixture field.

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
`work/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/03-cloud-virtual-networks-routes-and-controls.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why should a cloud subnet not be assumed to behave like an Ethernet VLAN?

2. How can stateful and stateless controls interact?

3. What part of a managed service path may remain outside customer visibility?
