# Route Selection, Filtering, and Redistribution

> **Module 1 · Section 5**

## Why It Matters

Route selection turns multiple candidates into installed reachability.
Filtering and redistribution connect routing domains but can also create leaks,
loops, and unstable feedback.

## Core Model

* Each protocol first selects its own best path, after which the routing
  process compares eligible sources for installation.

* Import policy controls accepted routes and attributes; export policy controls
  what is advertised to a peer.

* Prefix filters should be explicit about exact and more-specific routes.

* Redistribution translates reachability between protocols but usually loses
  some native topology meaning.

* Mutual redistribution without tags, filtering, or clear ownership can feed
  routes back into their origin.

## Reasoning Process

1. List candidates by prefix, source protocol, attributes, and next-hop
   validity.

2. Apply protocol-specific selection before cross-protocol preference.

3. Apply import, export, and redistribution policy at named boundaries.

4. Test route withdrawal and feedback behavior, not only initial advertisement.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-05-dynamic-routing
   touch work/module-01-operational-networking/section-05-dynamic-routing/04-route-selection-filtering-and-redistribution.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Route
   Selection, Filtering, and Redistribution** in
   `work/module-01-operational-networking/section-05-dynamic-routing/04-route-selection-filtering-and-redistribution.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/routing/ospf.json
   jq '.' labs/fixtures/routing/bgp.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Route Selection,
   Filtering, and Redistribution**. Apply the numbered Reasoning Process in
   order. For each step, cite at least one exact command result and label the
   statement as an observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* OSPF has two equal-cost paths to `10.0.20.0/24`, each with total cost 20.

* The BGP path through peer `192.0.2.2` has higher local preference 200 and is
  preferred despite its longer AS path.

* After the modeled link failure, the remaining OSPF next hop is installed 80
  milliseconds after detection and existing ECMP flows are rehashed.

## Completion Standard

Submit
`work/module-01-operational-networking/section-05-dynamic-routing/04-route-selection-filtering-and-redistribution.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a route be accepted but not installed?

2. What is the difference between an import filter and an export filter?

3. How can redistribution cause a routing loop without repeating an IP hop
   immediately?
