# Dependencies, Redundancy, and Failure Domains

> **Module 2 · Section 6**

## Why It Matters

A visible data path is only one part of service availability. Hidden control,
identity, naming, management, power, and provider dependencies shape real
failure domains.

## Core Model

* Direct dependencies lie on the packet path; indirect dependencies enable
  configuration, authentication, discovery, time, or recovery.

* Redundant data paths can share controllers, credentials, software,
  facilities, or management networks.

* A component can be available while a required dependency is degraded or
  unreachable.

* Failure domains should be defined from the service perspective, not device
  category.

* Recovery dependencies deserve the same scrutiny as steady-state dependencies.

## Reasoning Process

1. Start with the service and list every required data and control dependency.

2. Group shared infrastructure and common operational ownership.

3. Fail each group and trace effects on delivery, detection, and recovery.

4. Rank dependencies by blast radius, detectability, and restoration
   difficulty.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-02-network-architecture/section-06-reading-a-network-architecture
   touch work/module-02-network-architecture/section-06-reading-a-network-architecture/03-dependencies-redundancy-and-failure-domains.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Dependencies, Redundancy, and Failure Domains** in
   `work/module-02-network-architecture/section-06-reading-a-network-architecture/03-dependencies-redundancy-and-failure-domains.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   sed -n '1,160p' labs/fixtures/architecture/enterprise.md
   column -s, -t labs/fixtures/architecture/traffic-flows.csv
   jq '.' labs/fixtures/architecture/components.json
   jq '.' labs/fixtures/routing/vrfs.json
   ```

4. In the output file, add a `## Architecture Analysis` section for
   **Dependencies, Redundancy, and Failure Domains**. Apply the numbered
   Reasoning Process in order. Tie every design or failure claim to a named
   component, boundary, route, policy, or fixture field.

5. Add an architecture table with the columns `component or boundary`,
   `intended role`, `dependency`, `failure effect`, `evidence`, and
   `uncertainty`. Cite exact fixture fields.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The diagram establishes named zones and relationships but relies on the flow
  table and VRF file for policy and route facts.

* Flow `F3` is the only listed enterprise-to-OT application flow allowed
  directly; flow `F4` is denied.

* The management path uses a distinct VRF and `jump-host-policy`, which must be
  shown as a management and trust boundary.

## Completion Standard

Submit
`work/module-02-network-architecture/section-06-reading-a-network-architecture/03-dependencies-redundancy-and-failure-domains.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited architecture facts, a forward and return-path or failure
explanation tied to this subsection, all knowledge-check answers, and one
explicitly labeled uncertainty.

## Check Your Understanding

1. Why can redundant firewalls still share a failure domain?

2. Which dependency is required only during recovery?

3. How does poor clock synchronization affect failure analysis?
