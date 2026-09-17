# Course Diagrams

The 23 figures teach packet paths, route decisions, failure behavior, and
limits of evidence. Each lesson includes a saved SVG, editable Mermaid,
and a text equivalent that supports the same task in terminal delivery.
Light exports have a white background; dark exports use a dark background.
Open either saved image without installing a renderer. Solution figures
belong after the corresponding attempt and reveal.

## Figure Index

| Figure | Lesson and editable source | Light | Dark |
| --- | --- | --- | --- |
| cloud | [Lesson](../modules/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/03-cloud-virtual-networks-routes-and-controls.md) | [SVG](cloud.svg) | [SVG](cloud.dark.svg) |
| evidence-predict | [Lesson](../challenges/05-suspicious-is-not-proven.md) | [SVG](evidence-predict.svg) | [SVG](evidence-predict.dark.svg) |
| evidence-worked | [Lesson](../facilitator/solutions.md) | [SVG](evidence-worked.svg) | [SVG](evidence-worked.dark.svg) |
| fhrp | [Lesson](../modules/module-02-network-architecture/section-02-enterprise-network-architecture/03-first-hop-redundancy-hsrp-and-vrrp.md) | [SVG](fhrp.svg) | [SVG](fhrp.dark.svg) |
| handoff-predict | [Lesson](../challenges/06-the-shift-handoff.md) | [SVG](handoff-predict.svg) | [SVG](handoff-predict.dark.svg) |
| incident-order | [Lesson](../facilitator/solutions.md) | [SVG](incident-order.svg) | [SVG](incident-order.dark.svg) |
| ipv6 | [Lesson](../modules/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/02-ipv6-and-neighbor-discovery.md) | [SVG](ipv6.svg) | [SVG](ipv6.dark.svg) |
| leaf-spine | [Lesson](../modules/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/01-leaf-spine-and-traffic-directions.md) | [SVG](leaf-spine.svg) | [SVG](leaf-spine.dark.svg) |
| mtu-predict | [Lesson](../challenges/02-the-transfer-that-stops.md) | [SVG](mtu-predict.svg) | [SVG](mtu-predict.dark.svg) |
| mtu-worked | [Lesson](../facilitator/solutions.md) | [SVG](mtu-worked.svg) | [SVG](mtu-worked.dark.svg) |
| packet-predict | [Lesson](../challenges/01-be-the-packet.md) | [SVG](packet-predict.svg) | [SVG](packet-predict.dark.svg) |
| packet-worked | [Lesson](../facilitator/solutions.md) | [SVG](packet-worked.svg) | [SVG](packet-worked.dark.svg) |
| public-tls | [Lesson](../labs/exemplars/README.md) | [SVG](public-tls.svg) | [SVG](public-tls.dark.svg) |
| recovery | [Lesson](../challenges/recovery.md) | [SVG](recovery.svg) | [SVG](recovery.dark.svg) |
| response-loop | [Lesson](../challenges/recovery.md) | [SVG](response-loop.svg) | [SVG](response-loop.dark.svg) |
| route-selection | [Lesson](../modules/module-01-operational-networking/section-03-layer-3-and-packet-forwarding/04-longest-prefix-next-hop-and-default-routes.md) | [SVG](route-selection.svg) | [SVG](route-selection.dark.svg) |
| routing-predict | [Lesson](../challenges/03-pull-one-link.md) | [SVG](routing-predict.svg) | [SVG](routing-predict.dark.svg) |
| routing-worked | [Lesson](../facilitator/solutions.md) | [SVG](routing-worked.svg) | [SVG](routing-worked.dark.svg) |
| shared-power | [Lesson](../challenges/04-resilience-budget.md) | [SVG](shared-power.svg) | [SVG](shared-power.dark.svg) |
| stp | [Lesson](../modules/module-01-operational-networking/section-02-layer-2-networking/05-spanning-tree.md) | [SVG](stp.svg) | [SVG](stp.dark.svg) |
| vxlan | [Lesson](../modules/module-02-network-architecture/section-05-modern-data-center-and-cloud-networking/02-underlays-overlays-vxlan-and-evpn.md) | [SVG](vxlan.svg) | [SVG](vxlan.dark.svg) |
| zones-predict | [Lesson](../challenges/04-resilience-budget.md) | [SVG](zones-predict.svg) | [SVG](zones-predict.dark.svg) |
| zones-worked | [Lesson](../facilitator/solutions.md) | [SVG](zones-worked.svg) | [SVG](zones-worked.dark.svg) |

## Authoring and Verification

Edit the tagged Mermaid fence in the lesson, then regenerate both exports.
Keep one question per figure. Label its scenario, source, observation point,
and exact frame/record where available. State when a drawing is conceptual
or configured. Label inferred relationships; arrows for evidence derivation,
physical connections, and dependencies must have distinct meanings.

Use words as well as color, short wrapped labels, `accTitle`, `accDescr`, and
a text equivalent outside the collapsed source. Put prediction diagrams in
the learner brief and worked diagrams at the solution reveal. Keep reserved
case answers out of learner previews. Include no remote images or scripts.
Mermaid's [accessibility documentation](https://mermaid.js.org/config/accessibility.html)
describes the embedded SVG title and description.

The saved manifest records every source path and SHA-256, both export hashes,
and renderer version. This offline check needs only Python:

```sh
python3 -B verification/render_diagrams.py
```

For maintainers, install the pinned renderer in ignored `work/`, and supply
an existing Chrome/Chromium executable. Learners do not need Node or Chrome
for diagrams. The installation below suppresses browser-download scripts.

```sh
npm install --prefix work/mermaid --cache work/npm-cache --ignore-scripts --no-audit --no-fund @mermaid-js/mermaid-cli@11.12.0
python3 -B verification/render_diagrams.py --render --browser '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

Unchanged source/export pairs are reused. After changing rendering options,
remove the affected manifest entries to force their regeneration. Inspect
light and dark exports at a normal reading width: text must remain readable,
labels must not overlap, and before/after panels must read in order. Check
text fallbacks separately in `./course`; SVG hashes cannot establish clarity.
The package checker verifies source/export synchronization after extraction.

## Visual Review Record

All 46 light/dark SVGs were rendered with Mermaid CLI 11.12.0 and inspected
in contact sheets on September 16, 2026. Local Chrome checks found SVG titles,
descriptions, and no text outside the canvas. Wide timelines were changed
to vertical layouts and before/after panels gained explicit transition edges.
This is authoring QA, not a learner comprehension or timing result; those
comparisons remain in the [pilot worksheet](../facilitator/pilot.md).
