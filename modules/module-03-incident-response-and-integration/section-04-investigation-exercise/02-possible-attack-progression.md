# Possible Attack Progression

> **Module 3 · Section 4**

## Why It Matters

The proposed progression—from DNS and external C2 through discovery,
credentials, lateral movement, server access, and attempted protected-network
access—is a hypothesis to test, not a prescribed story.

## Core Model

* Each proposed step has prerequisites and should produce specific network,
  endpoint, identity, or control evidence.

* A later observation does not prove every earlier step occurred.

* Benign administrative, monitoring, update, or user behavior can produce
  portions of the same sequence.

* Multiple hosts or identities may participate, and one identifier can change
  through DHCP, VPN, NAT, or reassignment.

* The order should be reconstructed from normalized evidence rather than
  diagram layout.

## Reasoning Process

1. Translate each proposed step into observable predictions and alternative
   explanations.

2. Search evidence independently for those predictions.

3. Connect steps only with shared identifiers, plausible timing, and causal
   support.

4. Remove, reorder, split, or reject steps when evidence requires it.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-04-investigation-exercise
   touch work/module-03-incident-response-and-integration/section-04-investigation-exercise/02-possible-attack-progression.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Possible Attack Progression** in
   `work/module-03-incident-response-and-integration/section-04-investigation-exercise/02-possible-attack-progression.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Possible
   Attack Progression**. Apply the numbered Reasoning Process in order. Tie
   every claim to a frame or log record and label it observed, inferred,
   hypothesized, or unknown.

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
`work/module-03-incident-response-and-integration/section-04-investigation-exercise/02-possible-attack-progression.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Which later event could occur without credential compromise?

2. How can address reassignment create a false progression?

3. What evidence would falsify the proposed C2 step?
