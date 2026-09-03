# Lateral Movement, Persistence, and Exfiltration

> **Module 3 · Section 3**

## Why It Matters

These behaviors describe movement to other systems, survival across
interruption, and unauthorized transfer of data. Each requires evidence beyond
mere connectivity.

## Core Model

* Lateral movement uses credentials, remote services, trust, or exploits to
  operate on another internal system.

* Persistence maintains access across reboot, credential change, process exit,
  or other disruption.

* Exfiltration transfers data outside an authorized boundary or to an
  unauthorized destination.

* Administrative tools, backups, replication, and remote support can resemble
  these behaviors.

* Claims should identify source process or identity, target, action, data,
  direction, authorization, and outcome.

## Reasoning Process

1. Establish that the source could reach the target and attempted a relevant
   service.

2. Use endpoint, authentication, and target evidence to determine whether
   remote execution or access succeeded.

3. Identify durable changes for persistence rather than only repeated
   connections.

4. For exfiltration, connect data staging, transfer, destination, volume, and
   authorization.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/04-lateral-movement-persistence-and-exfiltration.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Lateral Movement, Persistence, and Exfiltration** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/04-lateral-movement-persistence-and-exfiltration.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Lateral
   Movement, Persistence, and Exfiltration**. Apply the numbered Reasoning
   Process in order. Tie every claim to a frame or log record and label it
   observed, inferred, hypothesized, or unknown.

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

* The evidence supports external periodic TLS and successful access to one SMB
  service, but it does not prove credential theft, remote execution,
  persistence, or data exfiltration.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/04-lateral-movement-persistence-and-exfiltration.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why is an SMB connection not by itself lateral movement?

2. What distinguishes persistence from a long-running process?

3. Can outbound volume alone prove exfiltration?
