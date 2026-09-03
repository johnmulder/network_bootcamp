# Tabletop Assessment Output

> **Module 2 · Section 7**

## Why It Matters

A useful tabletop output is a decision record, not a transcript. It connects
affected services, observations, blast radius, recovery, and design
improvements.

## Core Model

* The output names the scenario and assumptions precisely.

* Affected flows and user-visible effects are separated from internal device
  symptoms.

* Evidence is mapped to collection points and confidence.

* Recovery steps include prerequisites, owner, risk, verification, and
  rollback.

* Design recommendations address the failure mechanism without adding
  unjustified complexity.

## Reasoning Process

1. Summarize normal design intent and the injected condition.

2. Build a state timeline from fault through recovery.

3. Record decisions, supporting evidence, and rejected alternatives.

4. Prioritize corrective actions by risk reduction, effort, and new complexity.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-07-architecture-tabletop
   touch work/module-02-network-architecture/section-07-architecture-tabletop/03-tabletop-assessment-output.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Tabletop Assessment Output** in
   `work/module-02-network-architecture/section-07-architecture-tabletop/03-tabletop-assessment-output.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   jq '.' labs/fixtures/architecture/wan.json
   jq '.' labs/fixtures/network/l2-control.json
   jq -c '.' labs/fixtures/routing/route-events.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **Tabletop
   Assessment Output**. Apply the numbered Reasoning Process in order. Tie every
   design or failure claim to a named component, boundary, route, policy, or
   fixture field.

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
`work/module-02-network-architecture/section-07-architecture-tabletop/03-tabletop-assessment-output.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can the report distinguish symptom, mechanism, and root cause?

2. Does every recovery action include a verification step?

3. Would the recommendation create a new shared dependency?
