# Packet Capture

> **Module 3 · Section 2**

## Why It Matters

A packet capture offers the most granular network evidence available at its
collection point, but it remains incomplete outside that point, time window,
direction, and encryption boundary.

## Core Model

* A capture can show frame and packet headers, protocol messages, size,
  ordering, timing, flags, retransmissions, and unencrypted payload.

* Capture location determines which addresses, encapsulations, translations,
  and directions are visible.

* Encryption hides application content while leaving selected metadata
  observable.

* Packet loss, snap length, offload, duplicate capture, clock error, and
  filtering can alter the record.

* A PCAP proves that the sensor recorded bytes; it does not by itself prove
  user intent, process identity, delivery beyond the sensor, or application
  success.

## Reasoning Process

1. Validate capture metadata, interface, filter, time range, link type, and
   completeness.

2. Identify the relevant tuple and reconstruct both directions or document the
   missing side.

3. Decode protocol behavior while accounting for retransmission, reassembly,
   and encryption.

4. Correlate with endpoint and infrastructure evidence before attributing
   activity.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/01-packet-capture.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Packet Capture** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/01-packet-capture.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Packet
   Capture**. Apply the numbered Reasoning Process in order. Tie every claim to
   a frame or log record and label it observed, inferred, hypothesized, or
   unknown.

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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/01-packet-capture.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What exactly does a SYN in a PCAP prove?

2. How can capture placement change the visible NAT tuple?

3. Why might a packet appear malformed because of endpoint offload?
