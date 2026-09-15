# Incident Lifecycle

> **Module 3 · Section 3**

## Why It Matters

The incident lifecycle organizes work from detection through recovery and
learning. Phases can overlap and repeat as evidence changes.

## Core Model

* Detection identifies behavior requiring attention; triage establishes
  validity, priority, and immediate risk.

* Investigation develops timelines and hypotheses; scoping identifies affected
  identities, assets, data, and time.

* Containment limits ongoing harm while considering business and safety
  consequences.

* Eradication removes the mechanism and persistence after scope is credible.

* Recovery restores service safely and monitors for recurrence.

* Lessons learned improve architecture, controls, telemetry, procedures, and
  ownership.

## Reasoning Process

1. Define current phase objectives and decision authority.

2. Maintain a shared fact set, timeline, scope, and action log.

3. Choose containment proportional to evidence, impact, and operational risk.

4. Verify eradication and recovery against explicit success criteria before
   closure.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/05-incident-lifecycle.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Incident Lifecycle** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/05-incident-lifecycle.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Incident
   Lifecycle**. Apply the numbered Reasoning Process in order. Tie every claim
   to a frame or log record and label it observed, inferred, hypothesized, or
   unknown.

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
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/05-incident-lifecycle.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why can containment begin before investigation is complete?

2. What makes recovery different from eradication?

3. When should scoping be revisited?
