# Scenario and Evidence Set

> **Module 3 · Section 4**

## Why It Matters

The investigation begins with a suspected workstation compromise and a
deliberately incomplete set of local architecture, network, infrastructure,
endpoint, identity, and asset evidence.

## Core Model

* The initial suspicion is a lead, not a confirmed compromise.

* The architecture and route fixtures establish expected paths but may contain
  omissions or stale assumptions.

* The PCAP, flow, DNS, firewall, proxy, VPN, authentication, endpoint, and SIEM
  data have different scopes.

* Asset and identity context determine ownership, expected behavior, value, and
  response authority.

* Evidence must remain read-only; analysis outputs should be stored separately
  with source provenance.

## Reasoning Process

1. Inventory every source, time range, collection point, format, and integrity
   fact.

2. Read the case lead without allowing its wording to become the conclusion.

3. Build the expected path and visibility map before correlating observations.

4. Create an evidence ledger that preserves source references and analyst
   transformations.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-04-investigation-exercise
   touch work/module-03-incident-response-and-integration/section-04-investigation-exercise/01-scenario-and-evidence-set.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Scenario and Evidence Set** in
   `work/module-03-incident-response-and-integration/section-04-investigation-exercise/01-scenario-and-evidence-set.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Scenario and
   Evidence Set**. Apply the numbered Reasoning Process in order. Tie every
   claim to a frame or log record and label it observed, inferred, hypothesized,
   or unknown.

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
  SMB client, recorded successful network authentication, and the SIEM alert.

* Direct user-to-OT HTTPS is denied at `16:08:00Z`; no fixture proves
  successful OT access, credential theft, persistence, or exfiltration.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-04-investigation-exercise/01-scenario-and-evidence-set.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which source is derived from another source in the set?

2. What important visibility is missing before analysis starts?

3. How will you prove a derived result came from a specific original file?
