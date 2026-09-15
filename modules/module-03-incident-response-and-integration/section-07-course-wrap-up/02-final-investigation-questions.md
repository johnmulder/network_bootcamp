# Final Investigation Questions

> **Module 3 · Section 7**

## Why It Matters

Eight recurring questions provide a disciplined starting point for any network
or incident problem.

## Core Model

* What should happen establishes intent and success criteria.

* How the network makes it happen establishes path, protocols, state, and
  dependencies.

* Where policy is enforced establishes control and ownership.

* What happened and how it is known establish observations and provenance.

* What remains unknown and which explanation fits establish uncertainty and
  hypotheses.

* The next action should reduce uncertainty or risk with the least disruption.

## Reasoning Process

1. Answer each question with a fact, labeled inference, or explicit unknown.

2. Attach a source and limitation to each factual answer.

3. Use conflicting answers to identify the next test.

4. Select an action only after identifying objective, risk, authority,
   validation, and rollback.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict which of what happened, why, and what next
can be fully answered.

Run from the repository root:

```sh
tshark -n -r labs/fixtures/pcaps/incident.pcap -Y 'tcp || dns' -T fields -E header=y -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e tcp.dstport -e tcp.flags -e tls.handshake.type -e dns.qry.name
jq '.' labs/fixtures/incident/endpoint.jsonl
```

## Expected Evidence and Worked Reasoning

ClientHello and process-to-DNS are observed in their respective sources;
process-to-socket and malicious purpose remain unresolved. The next evidence
request should target one gap.

## Completion Standard

Answer each investigation question with a citation, inference, or explicit
unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. Which answer is based only on intended configuration?

2. What unknown most limits the conclusion?

3. Does the proposed action reduce risk, uncertainty, or both?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[NIST SP 800-86 §§3, 6 — forensic process and network traffic](https://csrc.nist.gov/pubs/sp/800/86/final)

[NIST SP 800-61r3 §2 — response in risk management](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
