# IOCs, IOAs, TTPs, and MITRE ATT&CK

> **Module 3 · Section 3**

## Why It Matters

Indicators and behavior frameworks organize evidence at different levels. They
support investigation and communication but should not replace direct
reasoning.

## Core Model

* An Indicator of Compromise is an observable artifact associated with
  malicious activity, such as a hash, domain, address, file, or registry value.

* An Indicator of Attack emphasizes behavior or conditions suggesting an active
  technique.

* Tactics, techniques, and procedures describe goals, methods, and
  actor-specific implementation patterns.

* MITRE ATT&CK provides a shared knowledge base for adversary tactics and
  techniques, not a verdict or exhaustive detection checklist.

* Indicators can be reused, shared, stale, spoofed, or seen in benign contexts;
  behavior and context determine meaning.

## Reasoning Process

1. Identify the observable and its source, time, scope, and confidence.

2. Classify it as artifact, behavior, technique, or contextual relationship.

3. Map behavior to ATT&CK only after evidence supports the technique.

4. Use the mapping to find coverage and next questions, not to inflate
   certainty.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/02-iocs-ioas-ttps-and-mitre-attack.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **IOCs,
   IOAs, TTPs, and MITRE ATT&CK** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/02-iocs-ioas-ttps-and-mitre-attack.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   jq -c '.' labs/fixtures/incident/siem.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   jq -c '.' labs/fixtures/incident/auth.jsonl
   jq -c '.' labs/fixtures/incident/flows.jsonl
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **IOCs, IOAs,
   TTPs, and MITRE ATT&CK**. Apply the numbered Reasoning Process in order. Tie
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

* The SIEM alert is created at `16:04:10Z` by `WORKSTATION-SMB-FANOUT`; it is
  an alert, not proof of an incident.

* Endpoint evidence places `update-agent` before `smb-client`, and
  authentication records a successful `svc-backup` network login to `file-01`
  from `10.0.10.23`.

* Frames 6, 10, and 14 show repeated TLS ClientHello messages. Frames 15–16
  show a TCP SYN/SYN-ACK on port 445; the authentication log separately
  records a successful network login. Completed TLS, file access, remote
  execution, credential theft, persistence, and exfiltration remain unproven.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/02-iocs-ioas-ttps-and-mitre-attack.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why is an IP address rarely sufficient proof of compromise?

2. What does an ATT&CK technique mapping establish?

3. How does an IOA differ from a static IOC?
