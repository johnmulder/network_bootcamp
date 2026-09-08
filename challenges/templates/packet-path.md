# My Packet-Path Sheet

Learner(s): ___

## Healthy Path — Challenge 1

<!-- artifact:start c01 -->

Prediction before inspection: ___

| Flow and observation point | Source/destination MAC | Source/destination IP | VLAN / VRF | Deciding table or state | Evidence / assumption |
| --- | --- | --- | --- | --- | --- |
| Local DNS exchange | | | | | |
| Request toward remote application | | | | | |
| Application reply at the observed trunk | | | | | |
| Unobserved downstream routing boundary | | | | | |

Dependency chain and what can be cached: ___

Route-selection reasoning and its effect on the path: ___

Return path: what is observed, what is predicted, and what evidence is missing?
___

<!-- artifact:end c01 -->

## Transfer Diagnosis — Challenge 2

<!-- artifact:start c02 -->

| Hypothesis | Expected observation | Actual evidence | Keep / reject / unresolved |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |

Header assumptions, mechanism, and what the calculated bound cannot prove: ___

Leading mechanism and confidence: ___

Repair proposal / owner / validation / rollback: ___

<!-- artifact:end c02 -->

## Link Failure — Challenge 3

<!-- artifact:start c03 -->

| State | Control-plane event | Forwarding consequence | What remains unproven |
| --- | --- | --- | --- |
| Normal | | | |
| Failure detected | | | |
| Table updated | | | |
| Later flow behavior | | | |

Why the route-selection rule matters here: ___

What differing contexts imply and what they do not establish: ___

<!-- artifact:end c03 -->

## Capstone Revision

<!-- artifact:start c06-path -->

Changed condition, forward and return decisions, and decisive record: ___

One claim I revised and the evidence that changed it: ___
<!-- artifact:end c06-path -->
