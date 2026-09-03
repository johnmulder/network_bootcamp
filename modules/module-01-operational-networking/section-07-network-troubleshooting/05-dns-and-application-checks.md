# DNS and Application Checks

> **Module 1 · Section 7**

## Why It Matters

After path and transport work, failures can remain in naming, TLS, proxies,
authentication, or application behavior. Testing by IP is useful but does not
reproduce the complete dependency chain.

## Core Model

* An application may use search domains, multiple record types, caches,
  proxies, or service discovery that command-line tests do not.

* A reachable IP with a failing hostname suggests a naming dependency but does
  not identify which resolver stage failed.

* TLS name validation and virtual hosting require the intended hostname even
  when the IP is reachable.

* Application errors can occur after successful TCP and TLS establishment.

* Endpoint and server logs may be required because network evidence cannot show
  encrypted application outcomes.

## Reasoning Process

1. Compare application behavior with direct name and address tests without
   assuming equivalence.

2. Confirm the resolver, answer, cache, and address the application actually
   used.

3. Trace TCP and TLS establishment for that exact destination and hostname.

4. Use endpoint or server evidence to interpret behavior beyond encrypted
   network visibility.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/05-dns-and-application-checks.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **DNS
   and Application Checks** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/05-dns-and-application-checks.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **DNS and Application
   Checks**. Apply the numbered Reasoning Process in order. For each step, cite
   at least one exact command result and label the statement as an observation
   or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The healthy baseline completes ARP, DNS, TCP, HTTP response, and orderly TCP
  close.

* The MTU case completes the handshake but fails after a 1400-byte payload and
  ICMP MTU 1200 response.

* The firewall evidence distinguishes an allowed translated egress session,
  allowed user-to-server SMB, and denied user-to-OT HTTPS.

## Completion Standard

Submit
`work/module-01-operational-networking/section-07-network-troubleshooting/05-dns-and-application-checks.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can connecting by IP produce a different TLS result?

2. What does a completed handshake prove about the application?

3. When is absence from a network capture expected rather than suspicious?
