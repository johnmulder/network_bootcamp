# Lateral Movement, Persistence, and Exfiltration

> **Module 3 · Section 3**

## Why It Matters

These behaviors describe movement to other systems, survival across
interruption, and unauthorized transfer of data. Each requires evidence beyond
mere connectivity.

## Core Model

* Lateral movement uses credentials, remote services, trust, or exploits to
  operate on another internal system.

* Persistence maintains access across reboot, credential change, process exit,
  or other disruption.

* Exfiltration transfers data outside an authorized boundary or to an
  unauthorized destination.

* Administrative tools, backups, replication, and remote support can resemble
  these behaviors.

* Claims should identify source process or identity, target, action, data,
  direction, authorization, and outcome.

## Reasoning Process

1. Establish that the source could reach the target and attempted a relevant
   service.

2. Use endpoint, authentication, and target evidence to determine whether
   remote execution or access succeeded.

3. Identify durable changes for persistence rather than only repeated
   connections.

4. For exfiltration, connect data staging, transfer, destination, volume, and
   authorization.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict whether successful network authentication
proves credential theft, remote execution, or file transfer.

Run from the repository root:

```sh
jq '.' labs/fixtures/incident/auth.jsonl
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
```

## Expected Evidence and Worked Reasoning

auth records svc-backup success to file-01, while port-445 packets stop at
SYN/SYN-ACK. No file audit, target process, or persistence change is supplied.

## Completion Standard

Separate authentication, remote operation, persistence, and exfiltration
claims.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Why is an SMB connection not by itself lateral movement?

2. What distinguishes persistence from a long-running process?

3. Can outbound volume alone prove exfiltration?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)
