# Endpoint and SIEM Telemetry

> **Module 3 · Section 2**

## Why It Matters

Endpoint telemetry ties network activity to processes, users, files, and host
state. A SIEM aggregates many sources but does not remove the need to
understand source semantics.

## Core Model

* EDR can connect sockets to process trees, command lines, hashes, users,
  files, and response actions.

* Endpoint coverage depends on agent health, platform support, policy,
  privileges, and retention.

* A SIEM normalizes, enriches, searches, and correlates events from multiple
  producers.

* Normalization can rename, drop, or transform fields; ingestion delay and
  collection failure can distort timelines.

* A correlation rule expresses a detection hypothesis and can combine weak
  signals without making them individually stronger evidence.

## Reasoning Process

1. Validate endpoint identity, agent health, policy, clock, and collection
   window.

2. Map network tuples to process, user, ancestry, and file evidence.

3. Trace SIEM fields back to raw source events and ingestion metadata.

4. Separate source fact, enrichment, correlation, analyst interpretation, and
   response action.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/05-endpoint-and-siem-telemetry.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Endpoint and SIEM Telemetry** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/05-endpoint-and-siem-telemetry.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/incident.pcap -T fields -E header=y -E separator=, -e frame.number -e frame.time_epoch -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e dns.qry.name -e dns.a -e tls.handshake.extensions_server_name
   mkdir -p work/zeek-incident
   (cd work/zeek-incident && zeek -r ../../labs/fixtures/pcaps/incident.pcap LogAscii::use_json=T)
   jq -c '.' work/zeek-incident/conn.log | sed -n '1,12p'
   jq -c '.' labs/fixtures/incident/flows.jsonl
   jq -c '.' labs/fixtures/incident/endpoint.jsonl
   ```

4. In the output file, add a `## Evidence Analysis` section for **Endpoint and
   SIEM Telemetry**. Apply the numbered Reasoning Process in order. Tie every
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

* The PCAP contains a DNS answer for `cdn-update.example.test`, three TLS
  ClientHello connections exactly 60 seconds apart, one answered SMB SYN, and
  two unanswered discovery SYNs.

* Zeek derives connection and DNS records from the same PCAP, so those records
  corroborate parsing but are not an independent observation source.

* Endpoint data connects `update-agent` to the DNS query and shows `smb-client`
  as its child; flow data summarizes four completed or observed conversations
  without payload.

## Completion Standard

Submit
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/05-endpoint-and-siem-telemetry.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Can endpoint telemetry prove a packet crossed a firewall?

2. Why should a SIEM field be traced to its source schema?

3. What does a healthy EDR agent fail to observe?
