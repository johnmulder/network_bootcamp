# Infrastructure Logs

> **Module 3 · Section 2**

## Why It Matters

DNS, DHCP, firewall, proxy, VPN, and authentication logs provide semantic
context unavailable in raw packets, but each reflects one product's decision
and logging policy.

## Core Model

* DNS logs connect clients, names, record types, answers, and resolver
  behavior, subject to cache and encrypted-resolution gaps.

* DHCP logs help map dynamically assigned addresses to clients over time.

* Firewall logs describe rule and session decisions at one boundary, often
  using translated tuples.

* Proxy logs can expose URLs, users, policy, and server outcomes when traffic
  actually traverses the proxy.

* VPN and authentication logs connect remote addresses, assigned addresses,
  identities, devices, factors, and session timing.

## Reasoning Process

1. Document log source, collection point, fields, time zone, retention, and
   logging conditions.

2. Normalize identifiers and timestamps before correlation.

3. Distinguish an attempted action, a policy decision, an established session,
   and successful application use.

4. Cross-check identity and address claims against lease, VPN, endpoint, and
   translation evidence.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-03-incident-response-and-integration/section-02-network-security-telemetry
   touch work/module-03-incident-response-and-integration/section-02-network-security-telemetry/03-infrastructure-logs.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Infrastructure Logs** in
   `work/module-03-incident-response-and-integration/section-02-network-security-telemetry/03-infrastructure-logs.md`.
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

4. In the output file, add a `## Evidence Analysis` section for **Infrastructure
   Logs**. Apply the numbered Reasoning Process in order. Tie every claim to a
   frame or log record and label it observed, inferred, hypothesized, or
   unknown.

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
`work/module-03-incident-response-and-integration/section-02-network-security-telemetry/03-infrastructure-logs.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a timeline or conclusion tied to this subsection,
claim-level confidence, all knowledge-check answers, one alternative
hypothesis, and one explicitly labeled visibility gap.

## Check Your Understanding

1. Does a firewall allow log prove application success?

2. Why can a DNS cache create no new resolver log for a connection?

3. Which records are needed to map a VPN-assigned address to a user at one
   time?
