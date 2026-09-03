# DNS Resolution, Delegation, and Caching

> **Module 1 · Section 4**

## Why It Matters

DNS is a distributed naming system and a frequent hidden dependency. Separating
resolver, authoritative, cache, and transport behavior prevents “DNS problem”
from becoming an unhelpful diagnosis.

## Core Model

* A stub resolver asks a recursive resolver, which may query root, top-level,
  and authoritative servers.

* Delegation uses NS records and glue where needed to direct queries toward
  authoritative servers.

* Answers, negative responses, and failures can be cached according to TTL and
  resolver policy.

* DNS commonly uses UDP but can retry over TCP; modern environments may also
  use encrypted transports.

* An answer can be syntactically successful but operationally wrong because of
  split views, stale caches, search domains, or application-specific
  resolution.

## Reasoning Process

1. Identify the querying process, stub configuration, recursive resolver, name,
   type, and search behavior.

2. Trace referral or cached-answer provenance to an authoritative source.

3. Interpret response code, answer section, TTL, and transport behavior.

4. Compare DNS output with the address the application actually attempted.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/03-dns-resolution-delegation-and-caching.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **DNS
   Resolution, Delegation, and Caching** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/03-dns-resolution-delegation-and-caching.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **DNS Resolution,
   Delegation, and Caching**. Apply the numbered Reasoning Process in order. For
   each step, cite at least one exact command result and label the statement as
   an observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The DNS answer maps `app.example.test` to `10.0.20.40`, followed by a TCP
  handshake and `GET /health` with HTTP status 200.

* The incident capture contains three TLS ClientHello records naming
  `cdn-update.example.test` at 60-second intervals.

* The DHCP fixture follows DISCOVER, OFFER, REQUEST, ACK and assigns address
  `10.0.10.23/24`, gateway `10.0.10.1`, and DNS `10.0.10.53`.

## Completion Standard

Submit
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/03-dns-resolution-delegation-and-caching.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. What is the difference between `NXDOMAIN` and an empty answer for one record
   type?

2. Why can two clients receive different valid answers for the same name?

3. Does a successful DNS response prove the application reached the returned
   address?
