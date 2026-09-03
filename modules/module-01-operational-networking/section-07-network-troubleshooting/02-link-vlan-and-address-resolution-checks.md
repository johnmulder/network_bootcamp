# Link, VLAN, and Address-Resolution Checks

> **Module 1 · Section 7**

## Why It Matters

The earliest forwarding dependencies are physical or logical link state, VLAN
membership, and neighbor resolution. Failures here should be proven before
investigating remote routing.

## Core Model

* Link state establishes only local connectivity; it does not prove correct
  VLAN, addressing, or end-to-end service.

* VLAN mismatches can isolate a host while leaving interfaces operational.

* ARP or Neighbor Discovery failure can result from wrong prefix, missing peer,
  filtering, duplicate addresses, or stale state.

* MAC and neighbor tables have age and observation-point limitations.

* Broadcast-domain symptoms should be separated from routed-path symptoms.

## Reasoning Process

1. Verify interface state, counters, and expected local attachment from
   fixture evidence.

2. Confirm effective VLAN on access and trunk links.

3. Check address, prefix, duplicate, and gateway assumptions.

4. Trace ARP or Neighbor Discovery and correlate it with switch learning.

## Teaching Instructions

1. From the repository root, verify the lab dataset and create the output
   file:

   ```sh
   python3 labs/build_fixtures.py --check
   mkdir -p work/module-01-operational-networking/section-07-network-troubleshooting
   touch work/module-01-operational-networking/section-07-network-troubleshooting/02-link-vlan-and-address-resolution-checks.md
   ```

2. Before examining the evidence, write one falsifiable prediction about **Link,
   VLAN, and Address-Resolution Checks** in
   `work/module-01-operational-networking/section-07-network-troubleshooting/02-link-vlan-and-address-resolution-checks.md`.
   State the exact fixture field, packet, or log record that would support or
   contradict it.

3. Run the evidence commands exactly as shown:

   ```sh
   tcpdump -nn -r labs/fixtures/pcaps/foundations.pcap
   tcpdump -nn -r labs/fixtures/pcaps/mtu-failure.pcap
   sed -n '1,120p' labs/fixtures/routing/macos-routes.txt
   jq -c '.' labs/fixtures/incident/firewall.jsonl
   ```

4. In the output file, add a `## Analysis` section for **Link, VLAN, and
   Address-Resolution Checks**. Apply the numbered Reasoning Process in order.
   For each step, cite at least one exact command result and label the statement
   as an observation or interpretation.

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
`work/module-01-operational-networking/section-07-network-troubleshooting/02-link-vlan-and-address-resolution-checks.md`.
It is complete when it contains the prediction, exact commands used, at least
three cited observations, a decision explanation tied to this subsection, all
knowledge-check answers, and one explicitly labeled uncertainty.

## Check Your Understanding

1. Why does an up interface not prove correct VLAN membership?

2. What evidence separates unanswered ARP from a missing route?

3. How can a duplicate address appear intermittent?
