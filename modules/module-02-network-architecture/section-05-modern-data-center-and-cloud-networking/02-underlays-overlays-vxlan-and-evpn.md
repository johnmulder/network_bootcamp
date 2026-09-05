# Underlays, Overlays, VXLAN, and EVPN

> Module 2 · Section 5 · Optional conceptual reference

## Purpose

Explain why a fabric can have working IP transport but broken tenant
connectivity. In the one-day course, use this as a recognition topic in the
[pocket reference](../../../challenges/reference.md). No separate submission
is required.

## Core Model

* The underlay supplies IP reachability between tunnel endpoints.
* VXLAN carries an Ethernet frame in UDP/IP; the VNI identifies a logical
  segment. Inner IP traffic still travels inside that Ethernet frame.
* A VTEP adds or removes the encapsulation at a tunnel endpoint.
* EVPN uses BGP to distribute overlay reachability such as MAC/IP information.
* A healthy underlay does not establish correct overlay mappings, tenant
  policy, or sufficient MTU after encapsulation.

## Conceptual Exercise

Use this explicitly hypothetical diagram, not the cloud route fixture:

```text
Host A -- VTEP A ===== routed IP underlay ===== VTEP B -- Host B
           |                                      |
           +------------ logical VNI 100 ----------+
```

1. Label the original endpoints, outer tunnel endpoints, and the distinction
   between underlay forwarding and overlay mapping.
2. Predict a symptom if the underlay route works but the remote MAC mapping is
   missing. Name the table and packet evidence you would request.
3. Explain why added encapsulation introduces a packet-size constraint even
   when the unencapsulated traffic previously fit.
4. Distinguish the VXLAN data-plane encapsulation from EVPN control-plane
   distribution. A VNI alone does not prove tenant authorization.

## Evidence Boundary and Self-Check

The repository's cloud route tables do not contain VNIs, VTEP mappings, EVPN
routes, or VXLAN packets. They cannot substantiate an encapsulation walkthrough.
This exercise practices a mental model only. A future fabric lab would need
those artifacts and a separately budgeted activity.

A satisfactory explanation identifies two different reachability questions:
can the outer packet reach the remote VTEP, and does the overlay know where the
inner destination belongs? It also identifies MTU and policy as independent
constraints. Keep any optional notes in your architecture assessment.
