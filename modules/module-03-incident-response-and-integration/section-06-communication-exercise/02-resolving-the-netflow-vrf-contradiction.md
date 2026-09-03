# Resolving the NetFlow and VRF Contradiction

> **Module 3 · Section 6**

## Why It Matters

The example claim—flow records show PLC VLAN traffic to an external address
while the VRF allegedly has no default route—contains an observation and a
configuration assertion that may both be true.

## Core Model

* The flow exporter location determines whether records describe original,
  routed, tunneled, proxied, or translated traffic.

* A VRF can reach a specific external prefix without a default route.

* Route leaking, policy routing, another routing table, proxying, NAT, a
  changed configuration, or mislabeled source can reconcile the statements.

* Flow records can be stale, sampled, mis-timestamped, duplicated, or
  attributed to the wrong interface.

* The absence of a current default route does not establish historical
  forwarding state.

## Reasoning Process

1. Define the exact flow fields, exporter, interfaces, observation domain, and
   time.

2. Identify the exact VRF and retrieve its relevant historical route
   information.

3. Test specific route, leak, proxy, NAT, policy-route, tunnel, and attribution
   explanations.

4. Request the smallest evidence set that distinguishes the remaining
   explanations.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-06-communication-exercise
   touch work/module-03-incident-response-and-integration/section-06-communication-exercise/02-resolving-the-netflow-vrf-contradiction.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Resolving the NetFlow and VRF Contradiction** in
   `work/module-03-incident-response-and-integration/section-06-communication-exercise/02-resolving-the-netflow-vrf-contradiction.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/flows.jsonl
   jq -c 'select(.dst == "198.51.100.77")' labs/fixtures/incident/firewall.jsonl
   jq '.OT' labs/fixtures/routing/vrfs.json
   jq -c '.' labs/fixtures/incident/proxy.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Resolving the
   NetFlow and VRF Contradiction**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* Flow data shows three connections from `10.0.10.23` to `198.51.100.77:443`;
  the enterprise firewall records translation to `192.0.2.44` under temporary
  egress rule `TEMP-EGRESS-17`.

* The OT VRF has no default route, but the observed external traffic originates
  in CORP, so the two statements are not actually contradictory.

* The proxy log records a temporary bypass, providing a precise owner and
  configuration question rather than a vague request to inspect the network.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-06-communication-exercise/02-resolving-the-netflow-vrf-contradiction.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why is a default route not required for every external destination?

2. Which observation could have occurred after the traffic left the VRF?

3. How would you test whether the source label is wrong?
