# Events, Alerts, Detections, and Incidents

> **Module 3 · Section 3**

## Why It Matters

Incident response depends on precise classification. Raw events, analytic
detections, alerts requiring attention, and confirmed incidents are related but
not interchangeable.

## Core Model

* An event is a recorded occurrence from a system, application, network, or
  security control.

* A detection is logic or analysis that identifies behavior matching a
  hypothesis or rule.

* An alert is a notification or case created for review, often from one or more
  detections.

* An incident is a confirmed or sufficiently credible security event requiring
  coordinated response under defined criteria.

* Triage decides priority and next action; it does not require complete
  root-cause certainty.

## Reasoning Process

1. Identify the raw event and source semantics.

2. Explain the analytic condition that produced the detection.

3. Determine why the detection generated an alert and what context it includes.

4. Apply the organization's incident criteria, impact, confidence, and urgency.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/01-events-alerts-detections-and-incidents.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Events, Alerts, Detections, and Incidents** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/01-events-alerts-detections-and-incidents.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Events,
   Alerts, Detections, and Incidents**. Apply the numbered Reasoning Process in
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
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/01-events-alerts-detections-and-incidents.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Can an alert be valid without representing an incident?

2. Why is an incident not merely a severe alert?

3. What information should triage establish first?
