# Failure-Scenario Patterns

> **Module 2 · Section 7**

## Why It Matters

Common failure patterns help organize a tabletop while preserving the
requirement to reason from architecture-specific evidence.

## Core Model

* Access failure isolates attached endpoints; distribution or core failure can
  affect broader routing, policy, or shared services.

* Firewall failure can lose sessions, NAT mappings, inspection, or symmetric
  paths even when a peer takes over.

* WAN failure can reveal hidden site dependencies, insufficient capacity, or
  ineffective health detection.

* Routing failure can create withdrawal, leak, blackhole, loop, asymmetry, or
  slow convergence.

* Shared-service, cloud-transit, and state-synchronization failures cross
  visible device boundaries.

## Reasoning Process

1. For each pattern, identify affected flows and the smallest expected blast
   radius.

2. Predict packet, route, session, and telemetry changes.

3. Compare full failure with one plausible partial failure.

4. Choose the safest discriminating test and recovery action.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-07-architecture-tabletop
   touch work/module-02-network-architecture/section-07-architecture-tabletop/02-failure-scenario-patterns.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Failure-Scenario Patterns** in
   `work/module-02-network-architecture/section-07-architecture-tabletop/02-failure-scenario-patterns.md`.
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
   **Failure-Scenario Patterns**. Apply the numbered Reasoning Process in order.
   Tie every design or failure claim to a named component, boundary, route,
   policy, or fixture field.

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
`work/module-02-network-architecture/section-07-architecture-tabletop/02-failure-scenario-patterns.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Which failure produces successful small transfers but failing large ones?

2. How can incorrect route advertisement outlive the original device fault?

3. Why can firewall state synchronization failure affect only established
   flows?
