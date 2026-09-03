# Telemetry Matrix and Comparison Exercise

> **Module 3 · Section 2**

## Why It Matters

The telemetry matrix forces every source to be evaluated by collection point,
strengths, limitations, retention, and evidentiary claim.

## Core Model

* Packet, flow, protocol, infrastructure, endpoint, and aggregated sources
  answer different questions.

* No source is universally strongest; usefulness depends on the claim being
  tested.

* Independent sources can corroborate a conclusion, while copied or derived
  sources are not independent.

* Conflicts can reveal clock, identity, path, transformation, or model errors.

* The matrix should identify the next best source when a claim exceeds current
  visibility.

## Reasoning Process

1. Process one saved PCAP with TShark and Zeek.

2. Correlate the results with named flow, infrastructure, endpoint, and SIEM
   events.

3. For each candidate claim, record which source proves, suggests, contradicts,
   or cannot address it.

4. Document conflicts and select the smallest additional evidence request.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/07-telemetry-matrix-and-comparison-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Telemetry Matrix and Comparison Exercise** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/07-telemetry-matrix-and-comparison-exercise.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Telemetry
   Matrix and Comparison Exercise**. Apply the numbered Reasoning Process in
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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/07-telemetry-matrix-and-comparison-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Did you mistake a derived Zeek log for independent corroboration of its
   source PCAP?

2. Which source best connects a network tuple to a process?

3. What additional source would resolve the most important conflict?
