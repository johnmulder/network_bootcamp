# Why Dynamic Routing Exists

> **Module 1 · Section 5**

## Why It Matters

Dynamic routing lets devices exchange reachability and adapt to topology
changes. Its value is not merely avoiding static routes; it provides a
distributed control system with explicit failure behavior.

## Core Model

* Routing protocols discover or advertise prefixes, select paths, and react
  when reachability changes.

* Convergence is the process by which participating devices reach a consistent
  usable view after a change.

* Fast convergence, stability, scale, policy, and path quality often trade
  against one another.

* A protocol route is control-plane information; the installed forwarding entry
  is a separate result.

* Dynamic routing can propagate mistakes quickly, so filtering, summarization,
  and ownership are design controls.

## Reasoning Process

1. Define which prefixes must be exchanged and between which administrative
   domains.

2. Identify the topology information or path attributes the protocol uses.

3. Describe route selection, installation, withdrawal, and convergence.

4. Bound the impact of incorrect advertisements with policy.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-05-dynamic-routing
   touch work/module-01-operational-networking/section-05-dynamic-routing/01-why-dynamic-routing-exists.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Why
   Dynamic Routing Exists** in
   `work/module-01-operational-networking/section-05-dynamic-routing/01-why-dynamic-routing-exists.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/routing/ospf.json
   jq '.' labs/fixtures/routing/bgp.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Why Dynamic Routing
   Exists**. Apply the numbered Reasoning Process in order. For each step, cite
   at least one exact command result and label the statement as an observation
   or interpretation.

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
`work/module-01-operational-networking/section-05-dynamic-routing/01-why-dynamic-routing-exists.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. What problem does dynamic routing solve that a static route does not?

2. Why can the best protocol route be absent from the forwarding table?

3. How can filtering reduce the blast radius of a mistake?
