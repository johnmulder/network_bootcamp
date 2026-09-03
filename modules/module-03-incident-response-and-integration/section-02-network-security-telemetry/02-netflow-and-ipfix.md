# NetFlow and IPFIX

> **Module 3 · Section 2**

## Why It Matters

Flow telemetry summarizes communications at much lower storage cost than packet
capture. It is powerful for scope and pattern analysis but omits payload and
often detailed protocol state.

## Core Model

* A flow record commonly includes source and destination addresses, ports,
  protocol, timestamps, counters, interfaces, and exporter context.

* Unidirectional records mean one conversation can produce separate forward and
  reverse entries.

* Active and inactive timeouts split long communication into multiple records.

* Sampling, aggregation, exporter placement, NAT, and templates affect
  precision and interpretation.

* Flow evidence can establish observed tuple, timing, and volume at an exporter
  but not application content or endpoint process.

## Reasoning Process

1. Identify exporter, observation domain, interfaces, template, sampling, and
   time basis.

2. Normalize records into forward and reverse groups using tuple and timing.

3. Account for timeout splits, NAT stages, duplicate exporters, and missing
   records.

4. Use patterns such as periodicity, fan-out, duration, and bytes as hypotheses
   rather than verdicts.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/02-netflow-and-ipfix.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **NetFlow and IPFIX** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/02-netflow-and-ipfix.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **NetFlow and
   IPFIX**. Apply the numbered Reasoning Process in order. Tie every claim to a
   frame or log record and label it observed, inferred, hypothesized, or
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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/02-netflow-and-ipfix.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Why can one TCP connection appear as several flow records?

2. What can byte counters suggest but not prove?

3. How does exporter location affect attribution through NAT?
