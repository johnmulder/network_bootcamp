# DHCP Address, Gateway, and DNS Assignment

> **Module 1 · Section 4**

## Why It Matters

DHCP supplies the network parameters that later routing and naming behavior
depend on. A valid lease can still contain an unusable address, gateway, or
resolver.

## Core Model

* DHCPv4 commonly follows Discover, Offer, Request, and Acknowledgment, with
  broadcast behavior during initial acquisition.

* A lease can provide address, mask or prefix, default gateway, DNS servers,
  domain information, and other options.

* Renewal normally becomes unicast when the client can reach the original
  server, then broadens during rebinding.

* Relay agents carry requests between broadcast domains and identify the client
  segment.

* Lease, relay, scope, reservation, and conflict evidence must be correlated by
  client identifier, MAC, address, and time.

## Reasoning Process

1. Identify the client, transaction identifier, requested address, and offered
   parameters.

2. Verify that the assigned address, prefix, gateway, and DNS options are
   internally consistent.

3. Determine whether a relay is present and which scope should answer.

4. Relate lease timing to the observed connectivity window.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/04-dhcp-address-gateway-and-dns-assignment.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **DHCP
   Address, Gateway, and DNS Assignment** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/04-dhcp-address-gateway-and-dns-assignment.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **DHCP Address, Gateway,
   and DNS Assignment**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

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
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/04-dhcp-address-gateway-and-dns-assignment.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can DHCP succeed while the client still cannot reach its gateway?

2. What role does a relay agent play?

3. Which timestamps matter when investigating an address that changed owners?
