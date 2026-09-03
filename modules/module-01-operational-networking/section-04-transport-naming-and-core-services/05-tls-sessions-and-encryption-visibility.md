# TLS Sessions and Encryption Visibility

> **Module 1 · Section 4**

## Why It Matters

TLS protects application data but leaves selected transport and handshake
metadata visible. Investigators must know where encryption begins and ends
before claiming what a sensor can prove.

## Core Model

* A TLS handshake negotiates protocol parameters, authenticates the server with
  certificates, and establishes traffic keys.

* Server Name Indication can expose the requested hostname in many TLS versions
  and configurations, while encrypted client hello can reduce that visibility.

* Certificates bind names to public keys through a trust chain and validity
  constraints; they do not prove the application is benign.

* After key establishment, payload content is encrypted, but addresses, ports,
  sizes, timing, and some handshake fields may remain observable.

* Proxies and load balancers can terminate and re-originate TLS, creating
  separate sessions and different observation points.

## Reasoning Process

1. Locate the TCP connection and identify the TLS handshake messages.

2. Record visible names, versions, cipher choices, certificate facts, and
   alerts.

3. Mark each encryption termination point on the architecture.

4. State precisely what remains observable at every sensor location.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/05-tls-sessions-and-encryption-visibility.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **TLS
   Sessions and Encryption Visibility** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/05-tls-sessions-and-encryption-visibility.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **TLS Sessions and
   Encryption Visibility**. Apply the numbered Reasoning Process in order. For
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
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/05-tls-sessions-and-encryption-visibility.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Does seeing a certificate prove which user initiated the connection?

2. Why can a proxy observe plaintext that a network tap cannot?

3. Which useful flow facts remain visible when payloads are encrypted?
