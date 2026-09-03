# TCP, UDP, Ports, and Sockets

> **Module 1 · Section 4**

## Why It Matters

Transport protocols connect application processes across IP networks. Ports
identify service endpoints, while sockets and tuples describe communication
from an operating-system or analytical viewpoint.

## Core Model

* TCP provides an ordered byte stream with connection state, reliability, flow
  control, and congestion control.

* UDP sends independent datagrams without transport-level delivery, ordering,
  or connection guarantees.

* A port identifies a transport endpoint within a host and protocol; TCP port
  53 and UDP port 53 are distinct.

* A listening socket accepts traffic for a local address and port, while an
  established socket includes both local and remote endpoints.

* Client source ports are usually ephemeral and are essential for
  distinguishing concurrent conversations.

## Reasoning Process

1. Identify IP protocol before interpreting port numbers.

2. Determine local and remote addresses and ports from the observation point.

3. Distinguish listening state from an established or one-way exchange.

4. Map the transport tuple to the owning process only when endpoint evidence
   supports it.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/01-tcp-udp-ports-and-sockets.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **TCP,
   UDP, Ports, and Sockets** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/01-tcp-udp-ports-and-sockets.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **TCP, UDP, Ports, and
   Sockets**. Apply the numbered Reasoning Process in order. For each step, cite
   at least one exact command result and label the statement as an observation
   or interpretation.

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
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/01-tcp-udp-ports-and-sockets.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why is a port number meaningless without a transport protocol and host?

2. What additional state does TCP maintain that UDP does not?

3. Why can multiple clients connect to the same server port simultaneously?
