# TCP Lifecycle and State

> **Module 1 · Section 4**

## Why It Matters

TCP's handshake, sequence space, acknowledgments, teardown, and resets reveal
whether a failure occurs before, during, or after connection establishment.

## Core Model

* The three-way handshake synchronizes initial sequence numbers and confirms
  bidirectional reachability.

* Sequence and acknowledgment numbers track bytes, not packets.

* Retransmissions can reflect loss, delay, reordering, capture gaps, or
  receiver behavior; context is required.

* FIN performs an orderly half-close, while RST immediately rejects or aborts a
  connection.

* Endpoints and stateful middleboxes can disagree about connection state
  because they observe different events or timeouts.

## Reasoning Process

1. Find SYN, SYN-ACK, and final ACK or identify the missing handshake step.

2. Follow sequence and acknowledgment progress through data transfer.

3. Interpret retransmissions alongside timing, window, and capture placement.

4. Determine which endpoint or middlebox sent FIN or RST and what preceded it.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/02-tcp-lifecycle-and-state.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **TCP
   Lifecycle and State** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/02-tcp-lifecycle-and-state.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **TCP Lifecycle and
   State**. Apply the numbered Reasoning Process in order. For each step, cite
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
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/02-tcp-lifecycle-and-state.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. What does a SYN retransmission establish and what does it not establish?

2. How can a firewall time out state while endpoints still believe a connection
   exists?

3. Why is a reset more informative when its sender and preceding packets are
   known?
