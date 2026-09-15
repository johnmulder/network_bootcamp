# Convergence and Route-Advertisement Exercise

> **Module 1 · Section 5**

## Why It Matters

Convergence analysis explains the transient interval between failure and stable
forwarding. The correct answer includes detection, withdrawal, calculation,
installation, and dependent-state effects.

## Core Model

* Failure detection can come from interface state, protocol timers,
  bidirectional detection, or missing keepalives.

* Information must propagate before remote devices can calculate a new route.

* Control-plane convergence and data-plane installation have distinct timing.

* ECMP changes can remap flows even when reachability remains available.

* Stateful middleboxes and applications may react more slowly or differently
  than routing.

## Reasoning Process

1. Establish the pre-failure best path and installed next hops.

2. Order detection, advertisement or withdrawal, calculation, and installation
   events.

3. Identify temporary blackholes, loops, or asymmetric paths.

4. State which flows recover automatically and which lose dependent state.

## Teaching Instructions

Use the [shared extended-study workflow](../../README.md#learning-workflow).
This task defines the required observations for this guide. The reasoning
checklist above is a general method: when device state is not supplied,
record it as unknown or explain a stated hypothetical; do not invent it.

**Predict and explain:** Predict the order of detection, propagation,
installation, and flow reassignment.

Run from the repository root:

```sh
jq '.' labs/fixtures/routing/route-events.jsonl
```

## Expected Evidence and Worked Reasoning

The log records fib_install 80 ms after link_down and a later flow_rehash. It
does not establish a measured blackhole interval or application recovery time.

## Completion Standard

Calculate the recorded interval and label other timing unknown.

Keep a prediction, the decisive citation or stated assumption, your revised
explanation, and one unresolved question in your existing module notes.
For optional separate notes, mirror this guide path under `work/`.
Knowledge checks below extend the conceptual model; unavailable device
state is a valid unknown, never a requirement to fabricate evidence.

## Check Your Understanding

1. What is the difference between detecting a failure and converging around it?

2. Can routing converge while an application connection remains broken?

3. How can ECMP membership change affect existing flows?

## Sources

Reviewed September 14, 2026. The exercise is self-contained and offline.
These references support the general model, not the fictional observations.

[RFC 2328 §§10, 16 — adjacency and route calculation](https://www.rfc-editor.org/rfc/rfc2328.html)
