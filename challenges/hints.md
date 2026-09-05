# Optional Hints

Open after a first attempt. Read one hint at a time, then return to the task.
Hints carry no penalty. This page contains partial worked steps; full answers
are in the separate [worked review](../facilitator/solutions.md).

## Challenge 1

1. Compare local DNS with the remote application at the same capture point.
2. Inspect `eth.dst` separately from `ip.dst`; a router is a local delivery
   target even when the IP destination is elsewhere.
3. In the independent CSV, `/32` is more specific than `/24`. Remove only the
   one host route, then repeat the match before considering preference.

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

1. Sort the supplied stages by event time, not by the general word “failover.”
2. `ospf_lsa`, `fib_install`, and `flow_rehash` describe different stages.
3. Subtract `15:20:00.000Z` from the table-install event to measure that stage.
   You would need a separate service observation to measure user recovery.

## Challenge 4

1. Begin with one required service and trace both directions.
2. Compare state synchronization, path health, and shared dependencies; their
   failure effects are not interchangeable.
3. Health monitoring can detect loss without repairing it. A transport backup
   can share power with the primary. State which requirement remains unmet.

## Challenge 5

1. Put each observation beside a source, entity, and timestamp.
2. A process-to-DNS event is not a process-to-socket event. A successful login
   records use of credentials, not their acquisition.
3. For the apparent VRF contradiction, find the source address and its context
   before asking whether OT needs a new default route.

## Challenge 6

1. Read the case's declared conditions before borrowing reference assumptions.
2. Look up the destination for the request, then the client address for the
   response, in the context active after the change.
3. A missing route and a firewall deny are different observations. A change
   explaining an outage still does not establish whether it was intentional.
