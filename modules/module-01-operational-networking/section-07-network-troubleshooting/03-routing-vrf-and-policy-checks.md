# Routing, VRF, and Policy Checks

> **Module 1 · Section 7**

## Why It Matters

Once local delivery works, the investigation moves to routing context, selected
paths, and policy boundaries. Configuration presence is not the same as packet
use.

## Core Model

* The lookup must occur in the routing table selected by the ingress context.

* Longest-prefix match and next-hop resolution determine forwarding before most
  downstream policy.

* ACL and firewall rules have direction, interface or zone, protocol, state,
  and order.

* A route can exist while policy denies traffic, and a permit can exist while
  no route reaches the destination.

* Logs may record only denials, only session creation, or a different
  observation tuple after NAT.

## Reasoning Process

1. Perform the forward and reverse route lookups in the correct contexts.

2. Place each policy evaluation on a specific interface, zone, or device.

3. Match the actual tuple and state to rule order and object expansion.

4. Correlate counters or logs with the test rather than relying on static text
   alone.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/03-routing-vrf-and-policy-checks.md
   ```

2. Before examining the evidence, write one falsifiable prediction about
   **Routing, VRF, and Policy Checks** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/03-routing-vrf-and-policy-checks.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Routing, VRF, and
   Policy Checks**. Apply the numbered Reasoning Process in order. For each
   step, cite at least one exact command result and label the statement as an
   observation or interpretation.

5. Add an evidence table with the columns `source`, `observation`,
   `interpretation`, and `uncertainty`. Cite exact frame numbers, prefixes,
   JSON fields, or log records.

6. Apply every step in the Reasoning Process, then answer all Check Your
   Understanding questions in the same output file.

## Expected Evidence

* The healthy baseline shows ARP, DNS, a TCP handshake, and an HTTP response.
  Frames 10–11 begin connection closure, but the final server ACK is absent;
  the capture does not establish completed TCP closure.

* The MTU case completes the handshake but fails after a 1400-byte payload and
  ICMP MTU 1200 response.

* The firewall evidence distinguishes an allowed translated egress session,
  allowed user-to-server SMB, and denied user-to-OT HTTPS.

## Completion Standard

Submit
`work/module-01-operational-networking/section-07-network-troubleshooting/03-routing-vrf-and-policy-checks.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why can a visible permit rule fail to match the packet?

2. How does the wrong VRF mimic a missing route?

3. What observation would prove the packet reached a policy boundary?
