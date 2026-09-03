# Route Isolation and Route Leaking

> **Module 1 · Section 6**

## Why It Matters

VRF isolation is the default absence of shared reachability. Route leaking
deliberately imports selected routes between contexts and must account for
return paths and policy.

## Core Model

* Isolation exists when no route in one context leads to the other, even if
  interfaces share a physical device.

* Route leaking can use static routes, shared services, import and export
  policies, or dedicated interconnection points.

* A leaked destination route without a corresponding return route creates
  one-way reachability.

* Shared service routes can unintentionally become transit paths if scope and
  policy are not constrained.

* Filtering, naming, NAT, and firewall behavior often interact with route
  leaking.

## Reasoning Process

1. Define the exact source and destination prefixes that require communication.

2. Select the controlled boundary where routes or traffic cross contexts.

3. Provide forward and return reachability without importing unrelated
   prefixes.

4. Apply policy and test whether either side can become unintended transit.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-06-vrfs-and-network-segmentation
   touch work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/02-route-isolation-and-route-leaking.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Route
   Isolation and Route Leaking** in
   `work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/02-route-isolation-and-route-leaking.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq 'to_entries[] | {vrf: .key, routes: .value}' labs/fixtures/routing/vrfs.json
   jq '.CORP, .OT, .MGMT' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Analysis` section for **Route Isolation and
   Route Leaking**. Apply the numbered Reasoning Process in order. For each
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
`work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/02-route-isolation-and-route-leaking.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why is leaking only the destination prefix often insufficient?

2. How can a shared-services VRF become a transit risk?

3. What is the difference between route visibility and policy permission?
