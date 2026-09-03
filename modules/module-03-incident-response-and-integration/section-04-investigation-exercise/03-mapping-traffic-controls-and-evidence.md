# Mapping Traffic, Controls, and Evidence

> **Module 3 · Section 4**

## Why It Matters

Every hypothesized step should be mapped to generated traffic, expected path,
encountered controls, observable telemetry, and residual artifacts.

## Core Model

* DNS, connection establishment, authentication, command execution, discovery,
  and transfer produce different traffic patterns.

* Routing and segmentation determine which controls can see or enforce each
  step.

* Policy and state affect initiation, return traffic, retries, and failure
  evidence.

* Network, endpoint, identity, and target logs should be correlated without
  treating shared derivation as independent proof.

* Failed actions can leave valuable evidence even when no session or
  application transaction completes.

## Reasoning Process

1. Define the exact source, destination, protocol, direction, and expected
   tuple for one step.

2. Trace path, policy, state, translation, encryption, and return behavior.

3. List expected evidence at every relevant collection point.

4. Compare expected and observed artifacts and explain discrepancies.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-04-investigation-exercise
   touch work/module-03-incident-response-and-integration/section-04-investigation-exercise/03-mapping-traffic-controls-and-evidence.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Mapping Traffic, Controls, and Evidence** in
   `work/module-03-incident-response-and-integration/section-04-investigation-exercise/03-mapping-traffic-controls-and-evidence.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   python3 labs/build_fixtures.py --check
   jq '.' labs/fixtures/incident/assets.json
   jq -c '.' labs/fixtures/incident/dns.jsonl
   jq -c '.' labs/fixtures/incident/flows.jsonl
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   jq -c '.' labs/fixtures/incident/auth.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   sed -n '1,12p' labs/fixtures/incident/evidence-ledger-template.csv
   ```

4. In the output file, add a `## Evidence Analysis` section for **Mapping
   Traffic, Controls, and Evidence**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `evidence ID`, `source`,
   `collection point`, `raw time`, `normalized time`, `entity`, `observation`,
   `classification`, `limitation`, and `confidence`. Cite exact frames or
   records.

6. Apply every step in the Reasoning Process, answer all Check Your
   Understanding questions, and keep at least one plausible alternative
   hypothesis in the same output file.

## Expected Evidence

* The checksum check passes before analysis, and the ledger template shows the
  required claim-classification and confidence fields.

* The evidence orders process start, DNS, three periodic TLS connections, child
  SMB client, successful SMB authentication, and the SIEM alert.

* Direct user-to-OT HTTPS is denied at `16:08:00Z`; no fixture proves
  successful OT access, credential theft, persistence, or exfiltration.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-04-investigation-exercise/03-mapping-traffic-controls-and-evidence.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Where would a denied connection leave evidence?

2. Which sensor sees the pre-NAT identity?

3. How can a failed authentication still support scoping?
