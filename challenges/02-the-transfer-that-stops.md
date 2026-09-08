<!-- delivery:start c02.brief -->
# The Transfer That Stops

**Module 1 · 45 minutes · Deliverable: `work/bootcamp/packet-path.md`**

The dashboard loads, but a separate diagnostic transfer to
`203.0.113.20:443` stalls. That is a reported symptom, not proof of a shared
root cause. Your mission is to identify the leading mechanism and the next
observation needed before recommending a repair.

Prerequisite: distinguish a TCP handshake from application success. Consult
the [reference card](reference.md) as needed. This is a constructed transfer
drill; port 443 and the dummy data do not establish a valid TLS session.
<!-- delivery:end c02.brief -->

<!-- delivery:start c02.predict -->
## Predict — 5 Minutes

Write three hypotheses, such as name resolution, path/policy, and packet size
or endpoint behavior. For each, predict an observation that would help rule
it out. You already know packets 1–3 form a TCP handshake. What does that
change, and what does it leave unresolved?
<!-- delivery:end c02.predict -->

<!-- delivery:start c02.inspect -->
## Inspect — 15 Minutes

Only after the prediction, read the neutral case capture:

```sh
tshark -n -r labs/fixtures/challenges/transfer.pcap
tshark -n -r labs/fixtures/challenges/transfer.pcap -Y 'tcp || icmp' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e ip.len -e ip.hdr_len -e tcp.hdr_len -e tcp.len -e tcp.seq -e tcp.options.mss_val -e icmp.type -e icmp.code -e icmp.mtu
```

Compare TCP data lengths and sequence numbers, not just frame lengths. ICMP
can contain a quoted copy of the original IP header, so its field output may
contain multiple IP values. Use the packet detail when you need to distinguish
the outer error packet from its quoted packet:

```sh
tshark -n -r labs/fixtures/challenges/transfer.pcap -Y 'icmp' -V
```

If the table is hard to read, use this decoded evidence after predicting:

| Frames | Recorded fields |
| --- | --- |
| 1–3 | TCP SYN, SYN-ACK, ACK; both SYN packets advertise MSS 1460 |
| 4 | TCP payload 1400 bytes; IP total length 1440; IP/TCP headers 20 bytes each |
| 5 | ICMP type 3, code 4; advertised next-hop MTU 1200 |
| 6 | Same TCP data sequence and length as frame 4, one second later |

These are alternate views of the same packets, not independent corroboration.
The observation point is a modeled VLAN 10 trunk.
<!-- delivery:end c02.inspect -->

<!-- delivery:start c02.calculate -->
## Calculate and Challenge — 15 Minutes

Make the factual attempt before opening a model result. Then choose a payload
and declared header scenario in the bounded transfer experiment. Predict whether
it fits; use `experiment_predict` then `experiment_result` (terminal `x`, `z`).
Compare a fitting small payload with the boundary. Explain why capacity does
not prove ICMP delivery or application recovery. If you need support, replace
part of this practice time with a worked example and fresh reassessment.

1. Calculate the largest TCP payload fitting the reported path limit with
   20-byte IPv4 and TCP headers, no options, and no encapsulation. State units.
2. Explain why the previously advertised MSS does not establish the entire
   path's capacity. What changes if additional headers are present?
3. Distinguish “ICMP existed at this capture point” from “the sender received
   and acted on ICMP.” Which observation would discriminate between a feedback
   delivery problem and endpoint handling?
4. Explain why completing the handshake does not rule out later policy,
   application, or size-dependent failures.

You may propose a host capture, endpoint PMTU state, or a controlled packet-size
comparison. Explain the result expected under each surviving hypothesis.
<!-- delivery:end c02.calculate -->

<!-- delivery:start c02.review -->
## Debrief and Checkpoint — 10 Minutes

Give the leading mechanism, decisive frames, one rejected hypothesis, and one
remaining uncertainty. Propose a repair with an owner, validation signal, and
rollback. The course asks for a proposal, not a change to your Mac's routes,
firewall, DNS, or MTU.

Pass when your explanation connects packet size, feedback, and retransmission
without claiming to know an unobserved endpoint configuration. Use
[hints](hints.md#challenge-2) or the
[worked review](../facilitator/solutions.md#challenge-2) after your attempt.

Next: [Pull One Link](03-pull-one-link.md).
<!-- delivery:end c02.review -->
