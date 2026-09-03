# Evidence Quality and Visibility Gaps

> **Module 3 · Section 2**

## Why It Matters

Evidence quality determines the strength of every conclusion. Coverage, timing,
loss, transformation, and retention must be evaluated before interpreting
content.

## Core Model

* Collection point defines the traffic or events eligible to be observed.

* Clock synchronization, time zones, timestamp precision, and ingestion delay
  affect ordering.

* Sampling, aggregation, deduplication, filtering, and parser behavior change
  granularity.

* Retention and rollover create historical gaps that cannot be repaired by
  searching harder.

* NAT, proxy, VPN, load-balancer, and tunnel transformations require
  correlation across identities.

* Sensor health and packet or log loss can make absence meaningless.

## Reasoning Process

1. For each source, document coverage, collection mechanics, clock,
   transformations, and retention.

2. Test source health during the relevant interval.

3. Quantify known loss, sampling, or truncation where possible.

4. State how each limitation changes confidence in specific claims.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/06-evidence-quality-and-visibility-gaps.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Evidence Quality and Visibility Gaps** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/06-evidence-quality-and-visibility-gaps.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Evidence
   Quality and Visibility Gaps**. Apply the numbered Reasoning Process in order.
   Tie every claim to a frame or log record and label it observed, inferred,
   hypothesized, or unknown.

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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/06-evidence-quality-and-visibility-gaps.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. When is absence of evidence meaningful?

2. How can clock skew reverse the apparent order of events?

3. Which transformation prevents direct tuple matching?
