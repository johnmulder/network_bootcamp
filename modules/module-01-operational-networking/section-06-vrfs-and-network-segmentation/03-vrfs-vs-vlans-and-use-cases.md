# VRFs vs. VLANs and Segmentation Use Cases

> **Module 1 · Section 6**

## Why It Matters

VLANs and VRFs segment different forwarding layers. They are often paired, but
neither is a substitute for policy or a complete security architecture.

## Core Model

* A VLAN separates Layer 2 forwarding and broadcast domains.

* A VRF separates Layer 3 routing tables and route visibility.

* One VRF can contain many VLAN-backed subnets, and VLAN identifiers can be
  reused in unrelated contexts.

* Segmentation use cases include tenants, management, production stages,
  partner access, overlapping acquisitions, and trust zones.

* Segmentation limits reachability; firewalls or ACLs are still needed where
  communication requires explicit policy.

## Reasoning Process

1. State whether the separation requirement concerns frames, routes, policy, or
   all three.

2. Choose VLAN, VRF, or both based on the required forwarding boundary.

3. Place controlled interconnection and telemetry points.

4. Test management access, shared services, failure behavior, and route
   leakage.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-06-vrfs-and-network-segmentation
   touch work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/03-vrfs-vs-vlans-and-use-cases.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **VRFs
   vs. VLANs and Segmentation Use Cases** in
   `work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/03-vrfs-vs-vlans-and-use-cases.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq 'to_entries[] | {vrf: .key, routes: .value}' labs/fixtures/routing/vrfs.json
   jq '.CORP, .OT, .MGMT' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Analysis` section for **VRFs vs. VLANs and
   Segmentation Use Cases**. Apply the numbered Reasoning Process in order. For
   each step, cite at least one exact command result and label the statement as
   an observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* `CORP` contains user, server, and default reachability; `OT` contains only
  `10.0.30.0/24` and `10.0.40.0/24`; `MGMT` contains management plus selected
  enterprise routes.

* `OT` has no default route and no route to `10.0.10.0/24`, so physical
  presence on the same device would not create reachability.

* A safe leak must specify both the exact destination and return reachability;
  importing the CORP default into OT would exceed the stated requirement.

## Completion Standard

Submit
`work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/03-vrfs-vs-vlans-and-use-cases.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Can two VLANs share one VRF?

2. Does placing systems in separate VRFs automatically inspect permitted
   traffic?

3. When is a VLAN boundary insufficient for route isolation?
