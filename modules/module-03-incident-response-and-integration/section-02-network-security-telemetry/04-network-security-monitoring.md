# Network Security Monitoring: Zeek, IDS, and IPS

> **Module 3 · Section 2**

## Why It Matters

Network security monitoring transforms traffic into protocol records,
detections, and sometimes prevention. Derived telemetry accelerates analysis
but inherits sensor and analytic limitations.

## Core Model

* Zeek produces protocol-oriented logs and connection summaries from observed
  traffic rather than preserving every packet as the primary interface.

* An IDS alert indicates a rule or analytic matched observed data; it is not
  automatically an incident.

* An IPS can block inline, making its action part of both security evidence and
  service availability.

* Signature, anomaly, and behavioral detection have different coverage, tuning,
  and false-positive characteristics.

* Encrypted traffic, packet loss, asymmetric capture, evasion, and
  protocol-parser gaps affect all network monitoring.

## Reasoning Process

1. Identify the sensor, mode, policy, rule or script version, and traffic
   coverage.

2. Trace the alert back to supporting connection, protocol, and packet
   evidence.

3. Test benign and malicious alternative explanations.

4. Determine whether the sensor observed, inferred, or actively changed the
   traffic.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/04-network-security-monitoring.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Network Security Monitoring: Zeek, IDS, and IPS** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/04-network-security-monitoring.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Network
   Security Monitoring: Zeek, IDS, and IPS**. Apply the numbered Reasoning
   Process in order. Tie every claim to a frame or log record and label it
   observed, inferred, hypothesized, or unknown.

5. Add an evidence-ledger table with the columns `source`, `raw time`,
   `normalized time`, `entity`, `observation`, `classification`, `limitation`,
   and `confidence`. Cite exact frames or records.

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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/04-network-security-monitoring.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. What does a Zeek connection state summarize?

2. Why is an IDS signature match not proof of compromise?

3. How does inline IPS placement change incident interpretation?
