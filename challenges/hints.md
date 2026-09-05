# Optional Hints

Open after a first attempt. Read one hint at a time, then return to the task.
Hints carry no penalty. This page contains partial worked steps; full answers
are in the separate [worked review](../facilitator/solutions.md).

## Challenge 1

<!-- delivery:start c01.hint1 -->
**Hint 1.** Compare local DNS with the remote application at the same capture
point.
<!-- delivery:end c01.hint1 -->

<!-- delivery:start c01.hint2 -->
**Hint 2.** Inspect `eth.dst` separately from `ip.dst`; a router is a local
delivery target even when the IP destination is elsewhere.
<!-- delivery:end c01.hint2 -->

<!-- delivery:start c01.hint3 -->
**Hint 3.** In the independent CSV, `/32` is more specific than `/24`. Remove
only the one host route, then repeat the match before considering preference.
<!-- delivery:end c01.hint3 -->

## Challenge 2

<!-- delivery:start c02.hint1 -->
**Hint 1.** Compare the first successful exchange with the first large data packet.
<!-- delivery:end c02.hint1 -->

<!-- delivery:start c02.hint2 -->
**Hint 2.** Inspect `tcp.len`, `ip.len`, repeated sequence numbers, and the
ICMP detail.
<!-- delivery:end c02.hint2 -->

<!-- delivery:start c02.hint3 -->
**Hint 3.** Subtract the two stated 20-byte headers from the reported 1200-byte path
   limit. That calculation does not tell you whether the endpoint received
   the ICMP packet you observed elsewhere.
<!-- delivery:end c02.hint3 -->

## Challenge 3

<!-- delivery:start c03.hint1 -->
**Hint 1.** Sort the supplied stages by event time, not by the general word
“failover.”
<!-- delivery:end c03.hint1 -->

<!-- delivery:start c03.hint2 -->
**Hint 2.** `ospf_lsa`, `fib_install`, and `flow_rehash` describe different
stages.
<!-- delivery:end c03.hint2 -->

<!-- delivery:start c03.hint3 -->
**Hint 3.** Subtract `15:20:00.000Z` from the table-install event to measure
that stage. You would need a separate service observation to measure user
recovery.
<!-- delivery:end c03.hint3 -->

## Challenge 4

<!-- delivery:start c04.hint1 -->
**Hint 1.** Begin with one required service and trace both directions.
<!-- delivery:end c04.hint1 -->

<!-- delivery:start c04.hint2 -->
**Hint 2.** Compare state synchronization, path health, and shared
dependencies; their failure effects are not interchangeable.
<!-- delivery:end c04.hint2 -->

<!-- delivery:start c04.hint3 -->
**Hint 3.** Health monitoring can detect loss without repairing it. A
transport backup can share power with the primary. State which requirement
remains unmet.
<!-- delivery:end c04.hint3 -->

## Challenge 5

<!-- delivery:start c05.hint1 -->
**Hint 1.** Put each observation beside a source, entity, and timestamp.
<!-- delivery:end c05.hint1 -->

<!-- delivery:start c05.hint2 -->
**Hint 2.** A process-to-DNS event is not a process-to-socket event. A
successful login records use of credentials, not their acquisition.
<!-- delivery:end c05.hint2 -->

<!-- delivery:start c05.hint3 -->
**Hint 3.** For the apparent VRF contradiction, find the source address and
its context before asking whether OT needs a new default route.
<!-- delivery:end c05.hint3 -->

## Challenge 6

<!-- delivery:start c06.hint1 -->
**Hint 1.** Read the case's declared conditions before borrowing reference
assumptions.
<!-- delivery:end c06.hint1 -->

<!-- delivery:start c06.hint2 -->
**Hint 2.** Look up the destination for the request, then the client address
for the response, in the context active after the change.
<!-- delivery:end c06.hint2 -->

<!-- delivery:start c06.hint3 -->
**Hint 3.** A missing route and a firewall deny are different observations. A
change explaining an outage still does not establish whether it was
intentional.
<!-- delivery:end c06.hint3 -->
