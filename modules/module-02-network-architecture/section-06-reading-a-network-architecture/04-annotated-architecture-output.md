# Annotated Architecture Output

> **Module 2 · Section 6**

## Why It Matters

The section output combines a diagram, flow table, boundary map, and
assumptions register into an artifact other disciplines can review.

## Core Model

* The base diagram should remain readable while annotations distinguish
  different boundary types.

* The flow table provides detail that arrows cannot: tuples, routes, policy,
  state, translation, encryption, and evidence.

* Facts, assumptions, and questions must use visibly different labels.

* Failure and visibility annotations should identify coverage and gaps rather
  than promise perfect resilience or monitoring.

* The artifact should be understandable without oral explanation.

## Reasoning Process

1. Select a consistent local Markdown notation and legend.

2. Annotate components, relationships, boundaries, dependencies, and redundant
   paths.

3. Attach detailed flow rows for the most important communications.

4. Review every claim against source material and collect unresolved questions.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-06-reading-a-network-architecture
   touch work/module-02-network-architecture/section-06-reading-a-network-architecture/04-annotated-architecture-output.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Annotated Architecture Output** in
   `work/module-02-network-architecture/section-06-reading-a-network-architecture/04-annotated-architecture-output.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/architecture/components.json
   jq '.' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Architecture Analysis` section for **Annotated
   Architecture Output**. Apply the numbered Reasoning Process in order. Tie
   every design or failure claim to a named component, boundary, route, policy,
   or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The diagram establishes named zones and relationships but relies on the flow
  table and VRF file for policy and route facts.

* The policy table intends direct enterprise-to-OT application flow `F3` to be
  allowed and `F4` to be denied. It does not establish live enforcement,
  complete routing, or successful delivery.

* The management path uses a distinct VRF and `jump-host-policy`, which must be
  shown as a management and trust boundary.

## Completion Standard

Submit
`work/module-02-network-architecture/section-06-reading-a-network-architecture/04-annotated-architecture-output.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Can a reader distinguish fact from assumption?

2. Are return paths and encryption termination visible?

3. Does the diagram remain usable after annotation?
