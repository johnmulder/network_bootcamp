# VRFs and Multiple Routing Tables

> **Module 1 · Section 6**

## Why It Matters

A VRF creates an independent routing context on a shared device. The same
address can therefore have different reachability and meaning depending on the
selected table.

## Core Model

* A VRF associates interfaces and routes with a separate routing and forwarding
  table.

* Routes in one VRF are not automatically visible in another or in the default
  routing table.

* Overlapping address space can be used across isolated VRFs because lookups
  occur in separate contexts.

* Management, tenant, production, or trust domains can use VRFs to limit route
  visibility.

* A device name alone is insufficient for troubleshooting; the ingress
  interface and selected VRF are required.

## Reasoning Process

1. Identify the ingress interface and its routing context.

2. Use only the routes present or deliberately imported into that context.

3. Resolve the chosen next hop within the correct context.

4. Repeat the analysis for the return direction and destination-side VRF.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-06-vrfs-and-network-segmentation
   touch work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/01-vrfs-and-multiple-routing-tables.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **VRFs
   and Multiple Routing Tables** in
   `work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/01-vrfs-and-multiple-routing-tables.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq 'to_entries[] | {vrf: .key, routes: .value}' labs/fixtures/routing/vrfs.json
   jq '.CORP, .OT, .MGMT' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Analysis` section for **VRFs and Multiple
   Routing Tables**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

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
`work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/01-vrfs-and-multiple-routing-tables.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can the same router produce different answers for one destination?

2. How do VRFs permit overlapping addresses?

3. What evidence identifies the routing context used by a packet?
