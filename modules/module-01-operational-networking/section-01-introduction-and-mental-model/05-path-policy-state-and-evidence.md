# Path, Policy, State, and Evidence

> **Module 1 · Section 1**

## Why It Matters

Most network questions become manageable when decomposed into four parts: where
traffic can go, whether it is allowed, what state it depends on, and what
observations prove the conclusion.

## Core Model

* Path is the sequence of forwarding decisions from source to destination and
  back.

* Policy determines permitted behavior through ACLs, firewalls, proxies,
  routing filters, and endpoint controls.

* State includes neighbor entries, routes, NAT mappings, transport connections,
  authentication, and middlebox sessions.

* Evidence is an observation with a source, collection point, timestamp, and
  known limitation.

* A conclusion is strongest when path, policy, state, and evidence agree;
  disagreement identifies the next investigation target.

## Reasoning Process

1. Write the expected forward and return paths.

2. At each boundary, identify the forwarding decision, policy check, and
   required state.

3. List the evidence expected from endpoints, network devices, and sensors.

4. Label every claim as observed, inferred, hypothesized, or unknown.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-01-introduction-and-mental-model
   touch work/module-01-operational-networking/section-01-introduction-and-mental-model/05-path-policy-state-and-evidence.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Path,
   Policy, State, and Evidence** in
   `work/module-01-operational-networking/section-01-introduction-and-mental-model/05-path-policy-state-and-evidence.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   sed -n '1,120p' labs/fixtures/architecture/enterprise.md
   python3 -m json.tool labs/fixtures/manifest.json | sed -n '1,80p'
   ```

4. In the output file, add a `## Analysis` section for **Path, Policy, State,
   and Evidence**. Apply the numbered Reasoning Process in order. For each step,
   cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The manifest reports the case name `network-bootcamp-reference` and 36
  checksum-protected fixture files.

* The architecture places `ws-23` at `10.0.10.23`, `file-01` at `10.0.20.40`,
  and the OT networks behind two explicit firewall boundaries.

* Your explanation identifies path, policy, state, and evidence as separate
  questions rather than treating the diagram as proof of live behavior.

## Completion Standard

Submit
`work/module-01-operational-networking/section-01-introduction-and-mental-model/05-path-policy-state-and-evidence.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does a permitted policy not prove a usable path exists?

2. Which state can make one direction work while the reverse initiation fails?

3. What evidence would distinguish a routing failure from a policy denial?
