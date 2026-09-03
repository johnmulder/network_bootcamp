# Application Dependency-Chain Exercise

> **Module 1 · Section 4**

## Why It Matters

An application request depends on local configuration, naming, routing,
transport, encryption, and application behavior. A dependency chain makes
hidden prerequisites and failure points explicit.

## Core Model

* The chain begins before the first application packet with local
  configuration, resolver state, routes, and potentially cached information.

* Each dependency produces different traffic and evidence, and some successful
  stages can be reused from cache.

* A visible application error may originate in a lower layer or in a separate
  shared service.

* Timeouts, reattempts, and fallback behavior can create multiple flows for one
  user action.

* The output must preserve ordering and distinguish required from optional
  dependencies.

## Reasoning Process

1. Start with the user action and list every prerequisite in execution order.

2. For each step, record traffic, created state, possible failure, and
   available evidence.

3. Mark cached, retried, fallback, or parallel behavior.

4. Use timestamps and tuples to connect the stages into one narrative.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-04-transport-naming-and-core-services
   touch work/module-01-operational-networking/section-04-transport-naming-and-core-services/06-application-dependency-chain-exercise.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Application Dependency-Chain Exercise** in
   `work/module-01-operational-networking/section-04-transport-naming-and-core-services/06-application-dependency-chain-exercise.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tshark -r labs/fixtures/pcaps/foundations.pcap -Y 'dns || http || tcp.flags.syn == 1' -T fields -E header=y -E separator=, -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.flags -e dns.qry.name -e dns.a -e http.request.uri -e http.response.code
   tshark -r labs/fixtures/pcaps/incident.pcap -Y 'tls.handshake.type == 1' -T fields -E header=y -E separator=, -e frame.time_relative -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
   jq -c '.' labs/fixtures/network/dhcp.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Application
   Dependency-Chain Exercise**. Apply the numbered Reasoning Process in order.
   For each step, cite at least one exact command result and label the statement
   as an observation or interpretation.

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
`work/module-01-operational-networking/section-04-transport-naming-and-core-services/06-application-dependency-chain-exercise.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Which stages may be absent from a capture because of caching?

2. How would a DNS failure differ from a TCP refusal in the evidence?

3. Did you separate user-visible symptoms from the failing dependency?
