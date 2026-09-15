# Alternative Explanations and Visibility Gaps

> **Module 3 · Section 4**

## Why It Matters

Strong investigations actively search for benign, accidental, and different
malicious explanations. Visibility gaps determine what cannot be concluded.

## Core Model

* Common alternatives include software updates, monitoring, backup, remote
  support, administrator behavior, misconfiguration, and compromised shared
  infrastructure.

* An alternative is useful when it predicts distinguishable evidence, not when
  it is merely possible.

* Visibility gaps can result from path, encryption, retention, sensor health,
  logging policy, unsupported protocols, or missing endpoint coverage.

* Correlated absence across healthy independent sources is stronger than
  absence from one uncertain source.

* Uncertainty should guide collection and action rather than be hidden by
  confident language.

## Reasoning Process

1. For every major claim, write at least one plausible alternative.

2. Identify evidence each explanation predicts differently.

3. Evaluate whether current sources had the ability and health to record it.

4. Select the additional artifact with the highest decision value and lowest
   collection risk.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-04-investigation-exercise
   touch work/module-03-incident-response-and-integration/section-04-investigation-exercise/04-alternative-explanations-and-visibility-gaps.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Alternative Explanations and Visibility Gaps** in
   `work/module-03-incident-response-and-integration/section-04-investigation-exercise/04-alternative-explanations-and-visibility-gaps.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Alternative
   Explanations and Visibility Gaps**. Apply the numbered Reasoning Process in
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
  SMB client, recorded successful network authentication, and the SIEM alert.

* Direct user-to-OT HTTPS is denied at `16:08:00Z`; no fixture proves
  successful OT access, credential theft, persistence, or exfiltration.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-04-investigation-exercise/04-alternative-explanations-and-visibility-gaps.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What makes an alternative hypothesis testable?

2. When does a visibility gap prevent a negative conclusion?

3. Which missing source has the highest decision value?
