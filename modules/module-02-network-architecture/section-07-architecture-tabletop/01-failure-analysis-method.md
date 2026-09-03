# Architecture Failure-Analysis Method

> **Module 2 · Section 7**

## Why It Matters

A tabletop tests design behavior before a real outage. It should reveal
dependencies, transient states, detection gaps, unsafe actions, and recovery
assumptions.

## Core Model

* A scenario states the initiating fault, scope, timing, and any concurrent
  conditions.

* Steady-state redundancy is less important than detection, convergence, state
  preservation, and operator response.

* Partial failures often produce more confusing behavior than total component
  loss.

* User-visible symptoms, telemetry, alarms, and administrative access may
  disagree.

* Recovery actions can enlarge impact if the model is wrong.

## Reasoning Process

1. Establish normal flows, ownership, state, and evidence.

2. Inject one precisely defined failure without silently adding others.

3. Trace immediate, transient, converged, and recovery states.

4. Record symptoms, evidence, decisions, risks, and unanswered questions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-07-architecture-tabletop
   touch work/module-02-network-architecture/section-07-architecture-tabletop/01-failure-analysis-method.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Architecture Failure-Analysis Method** in
   `work/module-02-network-architecture/section-07-architecture-tabletop/01-failure-analysis-method.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   jq '.' labs/fixtures/architecture/wan.json
   jq '.' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for
   **Architecture Failure-Analysis Method**. Apply the numbered Reasoning
   Process in order. Tie every design or failure claim to a named component,
   boundary, route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The access-switch failure affects only `ws-23`, while the stale firewall
  synchronization condition affects established NAT sessions.

* The WAN failure is degradation rather than link-down, so interface state
  alone would not trigger a correct diagnosis.

* The route event sequence installs the remaining next hop before recording
  flow rehash, exposing a transient state distinct from the steady-state
  design.

## Completion Standard

Submit
`work/module-02-network-architecture/section-07-architecture-tabletop/01-failure-analysis-method.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Did the scenario distinguish hard failure from partial degradation?

2. What evidence arrives first and which can mislead?

3. Could the proposed recovery action worsen the outage?
