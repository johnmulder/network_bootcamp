# Module 2 Architecture Assessment Review

> **Module 2 · Section 8**

## Why It Matters

The review demonstrates the ability to explain an architecture's design
decisions, boundaries, dependencies, and failure modes without overstating
incomplete diagrams.

## Core Model

* The assessment begins with requirements and important traffic flows.

* Layer 2, Layer 3, trust, security, failure, management, and visibility
  boundaries are explicit.

* Redundancy is tested against shared dependencies and transient behavior.

* Cloud, WAN, management, and OT relationships are included when relevant.

* Confirmed facts, assumptions, risks, and high-value questions remain
  distinct.

## Reasoning Process

1. Establish diagram scope, authority, and missing information.

2. Trace representative forward and return flows.

3. Evaluate boundaries, dependencies, policy, telemetry, and failure behavior.

4. Write a concise assessment with evidence, risks, questions, and next
   actions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-08-module-review
   touch work/module-02-network-architecture/section-08-module-review/01-architecture-assessment-review.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Module 2 Architecture Assessment Review** in
   `work/module-02-network-architecture/section-08-module-review/01-architecture-assessment-review.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/architecture/components.json
   jq -c '.' labs/fixtures/architecture/failures.jsonl
   ```

4. In the output file, add a `## Architecture Analysis` section for **Module 2
   Architecture Assessment Review**. Apply the numbered Reasoning Process in
   order. Tie every design or failure claim to a named component, boundary,
   route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* A complete assessment distinguishes diagram facts from route, policy,
  component, and failure facts stored in separate sources.

* The architecture contains at least five boundary types: Layer 3, trust,
  security, management, and visibility.

* The final review identifies the stale firewall state and degraded WAN as
  partial failures whose symptoms cannot be inferred from device-up status.

## Completion Standard

Submit
`work/module-02-network-architecture/section-08-module-review/01-architecture-assessment-review.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Did you explain why major boundaries exist?

2. Which common-mode failure defeats the apparent redundancy?

3. What question would most change your risk assessment?
