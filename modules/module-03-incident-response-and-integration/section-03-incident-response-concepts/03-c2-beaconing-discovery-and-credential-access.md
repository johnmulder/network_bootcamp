# C2, Beaconing, Discovery, and Credential Access

> **Module 3 · Section 3**

## Why It Matters

Early post-compromise behavior can appear as external command and control,
periodic communication, internal enumeration, and attempts to obtain
credentials.

## Core Model

* Command and control is communication used to direct or manage compromised
  systems; it can use common protocols and services.

* Beaconing is repeated communication with timing or size regularity, but
  software updates and monitoring can look similar.

* Discovery gathers information about hosts, accounts, services, shares, or
  network structure.

* Credential access seeks passwords, tokens, hashes, tickets, keys, or session
  material.

* Network evidence shows communication patterns and destinations, while
  endpoint evidence is often required to establish command, process, and
  credential actions.

## Reasoning Process

1. Measure timing, tuple, volume, protocol, and destination history for
   suspected C2.

2. Compare periodicity with benign service behavior and endpoint process
   context.

3. Map internal fan-out or service access to plausible discovery goals.

4. Seek endpoint and identity evidence before claiming credential access.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-03-incident-response-concepts
   touch work/module-03-incident-response-and-integration/section-03-incident-response-concepts/03-c2-beaconing-discovery-and-credential-access.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **C2,
   Beaconing, Discovery, and Credential Access** in
   `work/module-03-incident-response-and-integration/section-03-incident-response-concepts/03-c2-beaconing-discovery-and-credential-access.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **C2, Beaconing,
   Discovery, and Credential Access**. Apply the numbered Reasoning Process in
   order. Tie every claim to a frame or log record and label it observed,
   inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

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
`work/module-03-incident-response-and-integration/section-03-incident-response-concepts/03-c2-beaconing-discovery-and-credential-access.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Does periodic traffic prove beaconing?

2. Which network pattern can suggest internal discovery?

3. Why is credential access difficult to prove from flow data alone?
