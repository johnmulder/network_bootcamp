# VRF Isolation Exercise

> **Module 1 · Section 6**

## Why It Matters

This exercise tests whether routing context is treated as a first-class part of
every forwarding decision.

## Core Model

* The same physical router can connect both systems while maintaining no route
  between their contexts.

* Interface membership determines the initial lookup table.

* Route leaks must be explicit and directional.

* Return reachability and policy must be evaluated separately.

* The output should identify the smallest safe change rather than proposing
  broad route sharing.

## Reasoning Process

1. Map each interface, subnet, and route to a named VRF.

2. Attempt the forward lookup using only the source context.

3. Attempt the reverse lookup using only the destination context.

4. Propose and evaluate the minimum leak and policy needed for the stated flow.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-06-vrfs-and-network-segmentation
   touch work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/04-vrf-isolation-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **VRF
   Isolation Exercise** in
   `work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/04-vrf-isolation-exercise.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq 'to_entries[] | {vrf: .key, routes: .value}' labs/fixtures/routing/vrfs.json
   jq '.CORP, .OT, .MGMT' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Analysis` section for **VRF Isolation
   Exercise**. Apply the numbered Reasoning Process in order. For each step,
   cite at least one exact command result and label the statement as an
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
`work/module-01-operational-networking/section-06-vrfs-and-network-segmentation/04-vrf-isolation-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Did you accidentally use a route from the default table?

2. Does the proposed change enable both directions?

3. What unrelated destinations become reachable after the leak?
