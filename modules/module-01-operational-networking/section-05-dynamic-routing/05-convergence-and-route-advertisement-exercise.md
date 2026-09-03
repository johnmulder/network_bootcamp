# Convergence and Route-Advertisement Exercise

> **Module 1 · Section 5**

## Why It Matters

Convergence analysis explains the transient interval between failure and stable
forwarding. The correct answer includes detection, withdrawal, calculation,
installation, and dependent-state effects.

## Core Model

* Failure detection can come from interface state, protocol timers,
  bidirectional detection, or missing keepalives.

* Information must propagate before remote devices can calculate a new route.

* Control-plane convergence and data-plane installation have distinct timing.

* ECMP changes can remap flows even when reachability remains available.

* Stateful middleboxes and applications may react more slowly or differently
  than routing.

## Reasoning Process

1. Establish the pre-failure best path and installed next hops.

2. Order detection, advertisement or withdrawal, calculation, and installation
   events.

3. Identify temporary blackholes, loops, or asymmetric paths.

4. State which flows recover automatically and which lose dependent state.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-05-dynamic-routing
   touch work/module-01-operational-networking/section-05-dynamic-routing/05-convergence-and-route-advertisement-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Convergence and Route-Advertisement Exercise** in
   `work/module-01-operational-networking/section-05-dynamic-routing/05-convergence-and-route-advertisement-exercise.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq '.' labs/fixtures/routing/ospf.json
   jq '.' labs/fixtures/routing/bgp.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Convergence and
   Route-Advertisement Exercise**. Apply the numbered Reasoning Process in
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
`work/module-01-operational-networking/section-05-dynamic-routing/05-convergence-and-route-advertisement-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. What is the difference between detecting a failure and converging around it?

2. Can routing converge while an application connection remains broken?

3. How can ECMP membership change affect existing flows?
