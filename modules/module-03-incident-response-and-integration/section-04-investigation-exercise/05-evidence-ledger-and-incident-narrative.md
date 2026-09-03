# Evidence Ledger and Incident Narrative

> **Module 3 · Section 4**

## Why It Matters

The investigation output must let another analyst reproduce the timeline,
challenge each claim, and understand scope, confidence, gaps, and recommended
action.

## Core Model

* The ledger records evidence identifier, source, collection point, raw
  timestamp, normalized time, entity, observation, and limitation.

* The narrative separates confirmed observations from inference and hypothesis.

* Confidence is attached to individual claims rather than the case as a whole.

* Scope includes affected and explicitly searched-but-not-found assets,
  identities, data, and intervals.

* Recommendations state evidence need, containment objective, operational risk,
  owner, validation, and rollback.

## Reasoning Process

1. Normalize and reference evidence without altering originals.

2. Build the timeline from observations before writing causal prose.

3. Group claims into confirmed, supported, unresolved, and contradicted
   findings.

4. Write the smallest defensible narrative and prioritize next evidence and
   containment.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-04-investigation-exercise
   touch work/module-03-incident-response-and-integration/section-04-investigation-exercise/05-evidence-ledger-and-incident-narrative.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Evidence Ledger and Incident Narrative** in
   `work/module-03-incident-response-and-integration/section-04-investigation-exercise/05-evidence-ledger-and-incident-narrative.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Evidence
   Ledger and Incident Narrative**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

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
`work/module-03-incident-response-and-integration/section-04-investigation-exercise/05-evidence-ledger-and-incident-narrative.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Can a reviewer trace every sentence to evidence or a labeled inference?

2. Does scope use a repeatable case definition?

3. Is the recommended containment proportionate and reversible?
