"""Authored decisions and small adapters to the existing course models."""

from __future__ import annotations

import hashlib
import csv
import json
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import delivery
import learning

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "labs/fixtures"


@dataclass
class Scene:
    id: str
    title: str
    prompt: str
    fields: list[dict]
    expected: dict
    explanation: str
    cards: list[dict]
    board: list[str]
    hint: str
    model: str = ""
    parameters: dict = field(default_factory=dict)

    def public(self) -> dict:
        # Expected values and worked explanations never enter the drawing API.
        return dict(id=self.id, title=self.title, prompt=self.prompt,
                    fields=self.fields, cards=self.cards, board=self.board)


def choice(key, label, options, *, multiple=False, count=None, record=False):
    return dict(key=key, label=label, options=options, multiple=multiple, count=count, record=record)


def text_field(key, label, kind="text"):
    return dict(key=key, label=label, type=kind)


def card(ident, source, label, *, category="Declared condition", point="unknown", parents=(), projection=None, section=None):
    return dict(id=ident, source=source, label=label, category=category,
                point=point, parents=list(parents), projection=projection, section=section)


def source_path(item):
    return ROOT / item["source"] if item["source"].startswith("packet_post/") else FIXTURES / item["source"]


def source_name(item):
    return str(source_path(item).relative_to(ROOT))


def experiment(model, parameters):
    baseline, _ = delivery.experiment_baseline(model)
    wb = delivery.workbench(1)
    return learning.experiment(model, parameters, baseline, wb.select_routes, wb.best_vrf_route)


ROUTES = card("routes", "routing/route-candidates.csv", "Independent route-candidate snapshot")
VRFS = card("vrfs", "routing/vrfs.json", "Separate VRF lookup snapshot")
ROUTE_BOARD = ["         PREFIX SORTING OFFICE", "", " @ Pip -> [ /32 ] -> [ .252 ]",
               "       -> [ /24 ] -> [ .253 ]", "                  -> [ .254 ]",
               "       -> [ /8  ] -> [ .254 ]", "       -> [ /0  ] -> [ .1   ]",
               "", "Logical choices, not physical cables.", "IP destination stays inside the parcel."]


@lru_cache(maxsize=1)
def scenes() -> dict[str, Scene]:
    result = {}
    for ident, condition, title in (
        ("route.host", "baseline", "A very specific address"),
        ("route.remove", "remove-host-route", "The /32 sign takes a holiday"),
    ):
        parameters = dict(condition=condition, destination="10.0.20.40")
        answer = experiment("routing", parameters)
        prompt = "Choose the winning prefix and EVERY eligible next hop for 10.0.20.40."
        if condition != "baseline":
            prompt = "Declared change: remove ONLY 10.0.20.40/32. " + prompt
        result[ident] = Scene(ident, title, prompt,
            [choice("prefix", "Winning prefix", ["0.0.0.0/0", "10.0.0.0/8", "10.0.20.0/24", "10.0.20.40/32"]),
             choice("hops", "All eligible next hops", ["10.0.10.1", "10.0.10.252", "10.0.10.253", "10.0.10.254"], multiple=True)],
            dict(prefix=answer["prefix"], hops=", ".join(answer["next_hops"])),
            "Choose the longest matching prefix first. Among equal prefixes compare preference and metric; "
            "retain every equal candidate. An eligible set does not identify the actual ECMP member used.",
            [ROUTES], [line.replace("[ /32 ]", "[ /32 X]") for line in ROUTE_BOARD] if condition != "baseline" else ROUTE_BOARD,
            "A longer matching prefix outranks a less-specific one. Check all rows tied at the winning prefix.",
            "routing", parameters)
    corp = experiment("routing", dict(condition="CORP", destination="198.51.100.77"))
    ot = experiment("routing", dict(condition="OT", destination="198.51.100.77"))
    result["route.vrf"] = Scene("route.vrf", "Two rooms, two route tables",
        "Separate VRF snapshot: look up 198.51.100.77 in CORP and OT. Do not carry over the CSV host route.",
        [choice("corp", "CORP winning prefix", ["no route", "0.0.0.0/0", "198.51.100.0/24"]),
         choice("ot", "OT winning prefix", ["no route", "0.0.0.0/0", "198.51.100.0/24"])],
        dict(corp=corp["prefix"], ot=ot["prefix"]),
        "CORP has a matching default route through 10.0.10.1. OT has no match in its supplied table. "
        "Physical coexistence does not merge routing contexts. Policy and return traffic remain unproven.",
        [VRFS], [" @ -> [ CORP sorting room ]", "   -> [ OT sorting room   ]", "",
                    "Same device; separate lookups.", "No automatic route sharing."],
        "Only use routes in the named context. An absent matching prefix is a valid result.")
    result["route.limits"] = Scene("route.limits", "Inspector Maybe requests a receipt",
        "You selected a route. Which claim is supported?",
        [choice("claim", "Choose the claim", ["The dashboard recovered", "Forwarding choice only; inspect policy, return path and application response", "All equal-cost paths carried this flow"])],
        dict(claim="Forwarding choice only; inspect policy, return path and application response"),
        "A route lookup supplies a forwarding choice. Establish enforcement, return routing/state and a "
        "successful application response separately. The receipt has not arrived yet.",
        [ROUTES, VRFS], [" [ lookup ] -> [? policy ] -> [? return ]", "                          -> [? service ]"],
        "Which observations are absent from a route table?")
    with (Path(__file__).with_name("assets") / "practice-routes.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    selected = delivery.workbench(1).select_routes("192.0.2.42", rows)
    result["route.transfer"] = Scene("route.transfer", "A fresh sorting tray",
        "New game-only authored table, separate from all factory snapshots: choose forwarding for 192.0.2.42. "
        "Apply the same rule; a nearby host route need not match this destination.",
        [choice("prefix", "Winning prefix", ["0.0.0.0/0", "192.0.2.0/24", "192.0.2.41/32"]),
         choice("hops", "All eligible next hops", ["198.51.100.1", "198.51.100.2", "198.51.100.3", "198.51.100.4"], multiple=True)],
        dict(prefix=selected[0]["prefix"], hops=", ".join(sorted(r["next_hop"] for r in selected))),
        "The /32 describes .41, not destination .42. The matching /24 beats default and retains .2 and .3 "
        "as equal candidates. The static default's smaller preference does not outrank specificity.",
        [card("fresh-routes", "packet_post/assets/practice-routes.csv", "Game-only transfer exercise, rows 1-4")],
        [" [new destination] -> [which rows match?]", "", "Apply the rule before comparing preference."],
        "First discard nonmatching routes. Then choose the longest match and retain equal next-hop choices.")
    result.update(parcel_scenes())
    result.update(resilience_scenes())
    result.update(bridge_scenes())
    result.update(incident_scenes())
    result.update(handoff_scenes())
    result.update(recovery_scenes())
    result.update(foundation_scenes())
    return result


def parcel_scenes():
    result = {}
    capture = card("transfer", "challenges/transfer.pcap", "Frames 1-6 of the transfer drill",
                   category="Recorded observation", point="modeled VLAN 10 trunk", parents=("challenges/transfer.pcap",), projection="transfer")
    for scenario, headers in (("plain", (20, 20)), ("tcp-options", (20, 32)), ("ip-options", (24, 32))):
        parameters = dict(scenario=scenario, payload=1160)
        model = experiment("transfer", parameters)
        ident = "parcel." + scenario
        result[ident] = Scene(ident, "The parcel that wouldn't fit: " + scenario,
            f"Declared size model: path IP MTU 1200 bytes, IPv4 header {headers[0]} bytes, "
            f"TCP header {headers[1]} bytes. Choose a parcel payload, predict if it fits, and give the largest possible payload.",
            [choice("payload", "Load payload (bytes)", ["128", "1144", "1160", "1161", "1400"]),
             choice("fits", "Will this packet fit?", ["yes", "no"]),
             text_field("maximum", "Maximum payload, with bytes", "bytes")],
            dict(payload="1160", fits="yes" if model["fits"] else "no", maximum=f"{model['maximum_payload']} bytes"),
            "The whole IP packet must fit: payload plus IPv4 and TCP headers. Ethernet framing is outside this "
            "IP-MTU calculation. A fit establishes only the size condition, not ICMP delivery or application recovery.",
            [capture], ["      THE MTU MAIL SLOT", "", " [IPv4] + [TCP] + [payload]", "", "    | declared limit: 1200 |",
                       "", "Select a parcel and predict.", "The slot is polite, not flexible."],
            "Subtract both declared headers from the MTU. Compare your chosen payload plus those headers to 1200.",
            "transfer", parameters)
    result["parcel.receipt"] = Scene("parcel.receipt", "A handshake is not a delivery receipt",
        "The saved drill completes a TCP handshake, then repeats a 1400-byte payload. The capture shows ICMP MTU 1200. What remains unknown?",
        [choice("claim", "Select the bounded conclusion", ["TLS and the report transfer succeeded", "The sender received the ICMP and adapted", "Sender receipt, adaptation and application recovery remain unproven"])],
        dict(claim="Sender receipt, adaptation and application recovery remain unproven"),
        "Observed ICMP is not proof of sender receipt. The constructed port-443 exchange contains dummy payload, "
        "not a verified TLS session. Request sender-side feedback and a successful large-transfer service observation.",
        [capture], ["[SYN] -> [SYN ACK] -> [ACK]", "", " [large payload] -> [?]", " [ICMP seen]     -> [? sender]"],
        "Separate what the capture saw from what the endpoint received and what the application completed.")
    return result


def bridge_scenes():
    ospf = card("ospf", "routing/ospf.json", "R1 normal next-hop snapshot")
    events = card("events", "routing/route-events.jsonl", "R1 event timeline, records 1-4", category="Recorded observation", point="modeled R1 logs")
    bgp = card("bgp", "routing/bgp.json", "Separate BGP advertisement model")
    wb = delivery.workbench(1)
    answers = {q["id"]: q["answer"] for q in wb.convergence_questions()}
    return {
        "bridge.predict": Scene("bridge.predict", "The bridge on tea break",
            "Declared failure: R1 loses its neighbor 10.255.0.2. Before opening the event timeline, "
            "predict the remaining eligible next hop toward 10.0.20.0/24.",
            [choice("hop", "Expected remaining next hop", ["10.255.0.2", "10.255.0.3", "both"])],
            dict(hop="10.255.0.3"), "The normal snapshot has two equal-cost choices. Removing the declared "
            "failed adjacency leaves .3 as the candidate. The event timeline will establish what was installed and when.",
            [ospf], ["  [R1] --X-- [.2 on tea break]", "       --?-- [.3]", "", "Prediction, not observed recovery."],
            "Identify which normal choice does not use the failed neighbor."),
        "bridge.clock": Scene("bridge.clock", "Four postcards from the control plane",
            "Inspect records 1-4 in order. Give the time from logged link-down to FIB installation, "
            "then identify whether that interval establishes application recovery.",
            [text_field("interval", "Logged interval (milliseconds or ms)", "milliseconds"),
             choice("service", "Application recovery proved?", ["yes", "no"])],
            dict(interval=answers["m1.convergence.interval"] + " milliseconds", service="no"),
            "The logged interval is 80 ms: link_down to fib_install. The LSA occurs at 50 ms and flow_rehash at "
            "120 ms. None measures pre-log detection delay, packet loss, session recovery or the first successful application response.",
            [events], [" [detect] -> [advertise]", "          -> [install] -> [rehash]", "", "Service recovery: ?"],
            "Subtract the link_down time from fib_install, not the last event. Ask which layer each event describes."),
        "bridge.bgp": Scene("bridge.bgp", "A shorter path loses the vote",
            "Separate BGP snapshot: choose the preferred accepted advertisement for 198.51.100.0/24 using its supplied attributes.",
            [choice("peer", "Preferred peer", ["192.0.2.1", "192.0.2.2", "192.0.2.3"])],
            dict(peer="192.0.2.2"), "Among the accepted advertisements for this prefix, .2 has higher local preference "
            "(200 versus 100). The shorter AS path does not decide this example. A rejected advertisement is not an installed route.",
            [bgp], [" [peer .1] -- [local preference?]", " [peer .2] -- [AS path?]", "", "Policy precedes this path-length tie."],
            "Compare accepted entries for the same prefix, then local preference before AS-path length.")
    }


def incident_scenes():
    def log(name, label, parents=()):
        return card(name, f"incident/{name}.jsonl", label, category="Recorded observation", parents=parents)
    first = [log("flows", "Flow records #1-4"), log("siem", "Derived SIEM alert #1", ("incident/flows.jsonl", "incident/endpoint.jsonl"))]
    second = [log("endpoint", "Endpoint records #1-3"), log("auth", "Authentication records #1-2"), log("dns", "DNS records #1-2")]
    third = [log("firewall", "Firewall records #1-3"), log("proxy", "Proxy record #1")]
    return {
        "crumbs.pattern": Scene("crumbs.pattern", "Round 1: suspicious crumbs",
            "Open the flow and derived alert cards. Classify the repeated external pattern, then choose two next "
            "sources and explain why their possible results would change your conclusion. Source choice is recorded, not graded.",
            [choice("claim", "What is established?", ["Confirmed malicious C2", "Repeated external flows; malicious intent remains a hypothesis"]),
             choice("sources", "Two next requests", ["endpoint", "auth", "dns", "firewall"], multiple=True, count=2, record=True)],
            dict(claim="Repeated external flows; malicious intent remains a hypothesis", sources="endpoint, auth"),
            "Periodicity can fit benign or malicious activity. The SIEM alert derives from flow and endpoint inputs; "
            "it is not an independent extra sensor. Your next-source ranking is kept in the journal.",
            first, [" [flows] ---+", "           +--> [SIEM alert]", " [endpoint]+", "", "Derived alert != independent witness."],
            "A pattern can justify investigation while intent remains unknown. Request evidence that distinguishes your hypotheses."),
        "crumbs.attribution": Scene("crumbs.attribution", "Round 2: a process is not a socket",
            "Correlate the endpoint, authentication and DNS cards. What is directly supported?",
            [choice("process", "Process attribution", ["update-agent made the DNS query; socket attribution remains unproven", "update-agent is proved to own every external flow"]),
             choice("auth", "Authentication implication", ["svc-backup authentication succeeded; theft and remote execution are not proved", "Successful authentication proves credential theft"])],
            dict(process="update-agent made the DNS query; socket attribution remains unproven", auth="svc-backup authentication succeeded; theft and remote execution are not proved"),
            "Endpoint #2 explicitly associates update-agent with the DNS query. Authentication #2 records a successful "
            "network login to file-01 from 10.0.10.23 as svc-backup. Timing alone does not map processes to sockets or prove theft.",
            second, [" [process] --observed--> [DNS query]", "      ?                 ?", " [socket]             [intent]"],
            "Read the exact event types. DNS-query attribution and socket attribution require different observations."),
        "crumbs.clock": Scene("crumbs.clock", "The clocks exchange postcards",
            "Normalize the alternate display 2026-08-15T10:04:01-06:00 to UTC. It is the same auth #2 timestamp, not another event.",
            [text_field("utc", "UTC timestamp, including Z or +00:00", "utc")],
            dict(utc="2026-08-15T16:04:01Z"), "UTC is six hours ahead of this -06:00 display. Equal timestamps do not "
            "prove causal order; the original incident supplies no measured clock-error bound.",
            [second[1]], [" [raw time] -> [UTC display]", "", "One timestamp; one source event."],
            "A negative UTC offset means local time is behind UTC. Preserve the original timestamp in your citation."),
        "crumbs.boundary": Scene("crumbs.boundary", "Round 3: the historian keeps its door",
            "Inspect firewall #1-3 and the proxy record. Reconcile the workstation's external flow with OT's absent default route.",
            [choice("source", "Observed external source context", ["CORP workstation, not OT", "OT necessarily escaped isolation"]),
             choice("scope", "Denied direct OT attempt", ["This attempt was denied; other paths and broader scope remain unproven", "All OT compromise is impossible"])],
            dict(source="CORP workstation, not OT", scope="This attempt was denied; other paths and broader scope remain unproven"),
            "Firewall #1 maps 10.0.10.23 to 192.0.2.44 under TEMP-EGRESS-17. Proxy #1 records BYPASS, not decryption "
            "or application success. Firewall #3 denies one direct user-to-OT attempt. Preserve evidence; choose a scoped action with its owner.",
            third + [VRFS], [" [CORP ws-23] -> [egress rule]", "           X-> [OT historian]", "", "One deny does not prove global safety."],
            "Locate the actual source before consulting its routing context. Keep a single deny separate from global scope.")
    }


def handoff_scenes():
    case = card("practice-cases", "packet_post/assets/handoff.json", "Game-only P1 declared drill", section="P1")
    second = card("practice-case-p2", "packet_post/assets/handoff.json", "Separate game-only P2 declared drill", section="P2")
    return {
        "handoff.predict": Scene("handoff.predict", "Before opening the case folder",
            "An approved health check previously succeeded and now times out. Record two possible mechanisms before "
            "opening the new game-only case. No mechanism is yet established; explain your next evidence request.",
            [choice("hypotheses", "Two candidate mechanisms", ["attachment/VLAN changed", "routing or policy changed", "application unavailable", "name-resolution failure"], multiple=True, count=2, record=True)],
            dict(hypotheses="attachment/VLAN changed, application unavailable"),
            "Your hypotheses are recorded rather than judged as a diagnosis. The next decision supplies explicit "
            "conditions and source observations. Revise the diagnosis when evidence warrants it.", [],
            [" [symptom] -> [? mechanism]", "           -> [? next evidence]"],
            "Choose competing explanations; state which result would make you revise each."),
        "handoff.attachment": Scene("handoff.attachment", "P1: the parcel is in the wrong room",
            "New game-only P1 drill. Use the declared conditions and P1-1 through P1-3 to identify the leading mechanism.",
            [choice("mechanism", "Leading mechanism", ["Unexpected access VLAN prevents intended local neighbor resolution", "TLS certificate expiry is demonstrated", "DNS failure is demonstrated"])],
            dict(mechanism="Unexpected access VLAN prevents intended local neighbor resolution"),
            "P1-1 places the client in VLAN 20 instead of intended VLAN 10. P1-2 observes unanswered gateway ARP "
            "and an incomplete neighbor entry. The literal-IP test does not require DNS. Why membership changed and post-repair service health remain unknown.",
            [case], [" [client /24] -> [VLAN 20?]", " intended 10    [ARP unanswered]"],
            "Compare attachment before and after, then connect that difference to the neighbor observation."),
        "handoff.action": Scene("handoff.action", "P1: leave an actionable note",
            "Select the proportionate handoff for P1. Changes are tabletop recommendations, not live actions.",
            [choice("action", "Next step", ["Disable every factory account immediately", "Network operations validates VLAN intent with the owner, restores approved membership, tests the service and keeps rollback", "Declare the service restored because a configuration was proposed"])],
            dict(action="Network operations validates VLAN intent with the owner, restores approved membership, tests the service and keeps rollback"),
            "Link the next step to P1-1/P1-2, get the service owner's approval for disruption, check client ARP "
            "and successful health-check responses, and restore the prior membership if the change causes unintended effects.",
            [case], [" [record] -> [owner] -> [approved change]", "                 -> [test] -> [rollback]"],
            "A usable handoff names evidence, operational effect, an owner, a success test and rollback."),
        "handoff.application": Scene("handoff.application", "P2: the reply is still bad news",
            "Independent game-only P2 drill: TCP/TLS complete, but matching client/server request IDs show HTTP 503 and backend unavailable. Who owns the next investigation?",
            [choice("owner", "Next investigation", ["Application owner investigates backend evidence; service recovery remains open", "Network route repair alone is proved sufficient", "Security declares eradication complete"])],
            dict(owner="Application owner investigates backend evidence; service recovery remains open"),
            "P2-1/P2-2 support an application-service failure after transport/TLS progress. They do not identify "
            "the backend's cause. Keep P1 and P2 separate. Write your final handoff in at most 150 words across the four debrief fields.",
            [second], [" [TCP ok] -> [TLS ok] -> [HTTP 503]", "", "A response can report a service failure."],
            "Name the owner of the remaining failed dependency, and retain the observed service result.")
    }


def recovery_scenes():
    recovery = card("recovery", "challenges/recovery.json", "Hypothetical post-assessment continuations RA/RB")
    return {"recovery.receipt": Scene("recovery.receipt", "Return receipt requested",
        "After the original assessed cases: compare the hypothetical RA and RB continuations. Which scoped service restoration is accepted?",
        [choice("closure", "Closure supported by observations", ["Both A and B; routes were restored", "A scoped restoration accepted; B application recovery remains open", "Neither; no service observations exist"])],
        dict(closure="A scoped restoration accepted; B application recovery remains open"),
        "RA3/RA4 pair 30/30 TLS and HTTP 200 checks with scoped owner acceptance. RB3 still shows HTTP 503 and "
        "backend unavailable; RB4 rejects service restoration. Neither repair proves compromise, eradication, or permanent global health.",
        [recovery], [" [RA change] -> [service test] -> [owner]", " [RB change] -> [service test] -> [owner]", "", "These are hypothetical continuations."],
        "Read the application result and owner's decision as well as the configuration change.")}


def later_missions():
    return [
        dict(id="bridge", title="The Bridge on Tea Break", character="R1's exceedingly punctual clerk", duration="8-12 minutes",
             flavor="The bridge filed its leave request exactly 50 milliseconds too late.", lesson="challenges/03-pull-one-link.md",
             intro="Separate control-plane learning, installed forwarding choices and application recovery. "
             "The R1 failure model is independent of the route-candidate sorting room. Work out a candidate first, then inspect its event timeline.",
             steps=["bridge.predict", "bridge.clock", "bridge.bgp"], stamp="Clocks Before Claims"),
        dict(id="crumbs", title="The Case of the Suspicious Crumbs", character="Inspector Maybe", duration="12-18 minutes",
             flavor="Inspector Maybe's magnifying glass has a very small question mark etched into it.", lesson="challenges/05-suspicious-is-not-proven.md",
             intro="Post-lesson practice on the original incident. Sources arrive in three rounds; a derived alert is "
             "not another independent witness. Classify bounded claims, rank requests and keep explanations provisional.",
             requires=["c05.review"], steps=["crumbs.pattern", "crumbs.attribution", "crumbs.clock", "crumbs.boundary"], stamp="Asked for the Right Evidence"),
        dict(id="handoff", title="Please Forward to the Next Shift", character="The incoming operator", duration="10-15 minutes",
             flavor="The next shift likes concise notes almost as much as warm tea.", lesson="challenges/06-the-shift-handoff.md",
             intro="Use new game-only drills P1/P2, not the course's reserved A/B cases. Record hypotheses first, inspect "
             "the supplied conditions, distinguish the operational owner, and leave a short evidence-backed handoff.",
             steps=["handoff.predict", "handoff.attachment", "handoff.action", "handoff.application"], stamp="The Next Shift Says Thanks"),
        dict(id="recovery", title="Return Receipt Requested", character="The service owner", duration="5-8 minutes",
             flavor="A configuration receipt is not the same as a delivery receipt.", lesson="challenges/recovery.md",
             intro="Open only after both original A/B attempts have current reviews. These hypothetical continuations "
             "supply new observations; never use them as evidence available to the original diagnosis.",
             requires=["c06.review", "exit.review"], steps=["recovery.receipt"], stamp="Tested Before Closing"),
        dict(id="foundations", title="Two Envelopes & the Directory Desk", character="Ada ARP and Dot, the directory owl", duration="8-12 minutes",
             flavor="Ada knows the local doors. Dot knows addresses. Neither promises anyone is home.", lesson="challenges/01-be-the-packet.md",
             intro="Optional foundation practice. An IP destination describes the final target; the outer frame "
             "addresses a local neighbor. A /24 host normally sends within its subnet directly, and uses a gateway for a remote subnet. "
             "Then compare independent DNS and application symptoms.",
             steps=["foundation.envelopes", "foundation.directory"], stamp="Two Envelopes, One Destination")]


def foundation_scenes():
    packet = card("foundations", "pcaps/foundations.pcap", "Foundations frames at the VLAN 10 trunk", category="Recorded observation",
                  point="modeled VLAN 10 trunk", parents=("pcaps/foundations.pcap",), projection="foundations")
    return {
        "foundation.envelopes": Scene("foundation.envelopes", "Ada's two envelopes",
            "Workstation 10.0.10.23/24 sends to local resolver 10.0.10.53 and remote app 10.0.20.40. "
            "Without unusual host routes, whose MAC goes on each outer frame? Which IP stays inside the app packet?",
            [choice("dns", "DNS frame destination", ["Local resolver MAC", "Gateway MAC"]),
             choice("remote", "Remote app frame destination", ["Remote server MAC", "Gateway MAC"]),
             choice("ip", "App packet IP destination", ["10.0.10.1", "10.0.20.40"])],
            dict(dns="Local resolver MAC", remote="Gateway MAC", ip="10.0.20.40"),
            "ARP resolves the local neighbor. For remote delivery the gateway MAC goes on the frame while the "
            "remote app IP remains inside. This capture's gateway is .1; do not borrow the independent CSV next hops.",
            [packet, card("dhcp", "network/dhcp.jsonl", "DHCP lease records #1-4", category="Recorded observation")],
            [" OUTER FRAME: [ local neighbor ]", " INNER PACKET: [ final IP target ]", "", "   @ -> [neighbor] -> [? later hop]"],
            "Compare the /24 subnet first. The next-hop link address and final IP address solve different problems."),
        "foundation.directory": Scene("foundation.directory", "Dot knows addresses, not availability",
            "Independent comparisons D2 and D4: distinguish a received NXDOMAIN answer from successful DNS/TCP followed by HTTP 503.",
            [choice("d2", "D2 says", ["Name does not exist in that DNS answer", "No DNS response was received"]),
             choice("d4", "D4 next investigation", ["Application service/backend evidence", "Assume DNS never replied"])],
            dict(d2="Name does not exist in that DNS answer", d4="Application service/backend evidence"),
            "D2 received NXDOMAIN, unlike a timeout. D4 resolves an address and completes TCP but receives HTTP 503. "
            "A useful next request targets the remaining application failure. These comparisons are separate from the factory incident.",
            [card("dns-comparisons", "network/troubleshooting.json", "Independent DNS comparisons D1-D4", section="dns")],
            [" [name] -> [address] -> [TCP] -> [app]", "", "Directory success is not service success."],
            "Read both the DNS response and the later application result. Each step proves a different condition.")
    }


def resilience_scenes():
    result = {}
    failures = card("failures", "architecture/failures.jsonl", "Declared tabletop failure outcomes")
    flows = card("flows", "architecture/traffic-flows.csv", "Intended service policy, not measured enforcement")
    for ident, failure, twist in (("budget.state", "session-sync-stale", False),
                                  ("budget.wan", "20-percent-loss", False),
                                  ("budget.twist", "power-loss", True)):
        parameters = dict(options=["state-sync", "monitoring"], failure=failure, twist=twist)
        result[ident] = Scene(ident, "Two tokens and a teapot" + (": shared-power twist" if twist else ""),
            f"Failure: {failure}. Spend exactly two fictional tokens on two improvements. "
            + ("New condition: both transports share building power; current management uses the preferred path. " if twist else "")
            + "Predict whether these choices alone establish successful service recovery, and explain your tradeoff.",
            [choice("options", "Spend two tokens", ["state-sync", "backup-path", "monitoring", "management"], multiple=True, count=2),
             choice("recovered", "Service recovery proven?", ["yes", "no"])],
            dict(options="state-sync, monitoring", recovered="no"),
            "The model reports dependencies targeted by your choices, not guaranteed repairs. Monitoring needs a "
            "measured polling/alert delay; paths need capacity and independence; state sync needs validation. "
            "No pair solves every requirement. Your written tradeoff remains for human review.",
            [failures, card("wan", "architecture/wan.json", "WAN conditions and measurement gaps"), flows],
            ["    THE RESILIENCE TEAPOT", "", "    (o) (o)  two brass tokens", "", " [state] [backup] [monitor] [mgmt]",
             "", "No token grants certainty."],
            "Choose two distinct improvements. State what they address and what they cannot establish. "
            "A second transport does not fix shared power.", "resilience", parameters)
    result["budget.policy"] = Scene("budget.policy", "The historian's invitation list",
        "Compare F3 and F4. Who is intended to reach historian 10.0.30.50 over HTTPS? What does that table prove?",
        [choice("source", "Intended permitted source", ["10.0.10.23", "10.0.20.40"]),
         choice("status", "Evidence strength", ["Intended permission; enforcement and return path need checks", "Live enforcement and service success proven"])],
        dict(source="10.0.20.40", status="Intended permission; enforcement and return path need checks"),
        "F3 intends to permit the server; F4 intends to deny the user workstation. Do not erase segmentation "
        "to earn availability points. A policy-intent table is not live-rule or successful-session evidence.",
        [flows], [" [user]   --?-- [OT boundary]", " [server] --?-- [historian]", "", "Intent needs enforcement evidence."],
        "Read the intended field for each source. A desired rule is not an observed rule decision.")
    return result


def missions() -> list[dict]:
    first = [dict(id="sorting", title="The Sorting Office", character="Pip & the prefix clerk",
        flavor="Small labels. Big opinions. Please sort the mail before the tea cools.",
        lesson="challenges/01-be-the-packet.md", duration="12-15 minutes",
        intro="In a separate worked example, destination 192.0.2.8 matches both 192.0.2.0/24 and "
              "192.0.2.8/32. The /32 is more specific. Our office chooses forwarding; it cannot promise "
              "a complete service path. Open evidence with E, then make your prediction.",
        steps=["route.host", "route.remove", "route.vrf", "route.transfer", "route.limits"], stamp="Return Address Included"),
        dict(id="parcel", title="The Parcel That Wouldn't Fit", character="The extremely polite MTU mail slot",
             flavor="The slot regrets that politeness cannot increase its aperture.", duration="8-12 minutes",
             lesson="challenges/02-the-transfer-that-stops.md",
             intro="A completed handshake does not prove a large report transferred. For a separate worked example, "
             "an IP MTU of 1000 and headers of 20 + 20 leave 960 bytes of payload. Now pack parcels against "
             "the declared 1200-byte limit. Your parameter choices change the computed result.",
             steps=["parcel.plain", "parcel.tcp-options", "parcel.ip-options", "parcel.receipt"], stamp="Mind the Headers"),
        dict(id="resilience", title="Two Tokens and a Teapot", character="The quarterly improvement committee",
             flavor="The teapot issues two tokens and declines all requests for a third.", duration="10-15 minutes",
             lesson="challenges/04-resilience-budget.md",
             intro="Keep useful services available without dropping their boundaries. Each improvement costs one "
             "fictional token, not a real procurement price. Choose two, predict, and compare dependencies addressed "
             "with residual risk. Several choices are defensible; your explanation matters.",
             steps=["budget.policy", "budget.state", "budget.wan", "budget.twist"], stamp="Budgeted for Doubt")]
    all_missions = {m["id"]: m for m in first + later_missions()}
    return [all_missions[key] for key in ("sorting", "parcel", "bridge", "resilience", "crumbs", "handoff", "recovery", "foundations")]


def mission(ident):
    return next(m for m in missions() if m["id"] == ident)


def evidence(item: dict) -> str:
    path = source_path(item)
    if item.get("projection"):
        projection = json.loads((Path(__file__).with_name("assets") / "observations.json").read_text())[item["projection"]]
        if hashlib.sha256(path.read_bytes()).hexdigest() != projection["sha256"]:
            raise ValueError("Decoded observation is stale; restore its matching source capture.")
        body = json.dumps(projection, indent=2)
    elif path.suffix == ".json":
        data = json.loads(path.read_text())
        if item.get("section"):
            data = dict(scope=data.get("scope", "Declared scope applies to this section only."), **{item["section"]: data[item["section"]]})
        body = json.dumps(data, indent=2)
    elif path.suffix == ".jsonl":
        body = "\n\n".join(f"#{i}: {line}" for i, line in enumerate(path.read_text().splitlines(), 1))
    else:
        body = path.read_text().strip()
    return (f"{item['category']} | {item['label']}\nScenario/source: {source_name(item)}\n"
            f"Observation point: {item['point']}\n"
            f"Derived from: {', '.join(item['parents']) or 'no derivation asserted'}\n\n{body}")


def evaluate(scene: Scene, values: dict) -> dict:
    if not isinstance(values, dict) or set(values) != {f["key"] for f in scene.fields}:
        raise ValueError("Complete each displayed field before committing.")
    checks = {}
    expected = dict(scene.expected)
    parameters = dict(scene.parameters)
    model = None
    for spec in scene.fields:
        key, response = spec["key"], values[spec["key"]]
        if spec.get("multiple"):
            if not isinstance(response, list) or not response or any(not isinstance(v, str) for v in response) or len(set(response)) != len(response):
                raise ValueError("Choose each eligible option once.")
            if any(v not in spec["options"] for v in response):
                raise ValueError("Choose displayed options.")
            if spec.get("count") and len(response) != spec["count"]:
                raise ValueError(f"Choose exactly {spec['count']} distinct improvements.")
            response = ", ".join(response)
        elif not isinstance(response, str) or not response.strip() or len(response) > 1600:
            raise ValueError("Complete each field (up to 1600 characters).")
        if "options" in spec and not spec.get("multiple") and response not in spec["options"]:
            raise ValueError("Choose a displayed option.")
        if scene.model == "transfer" and key == "payload":
            parameters["payload"] = int(response)
            model = experiment("transfer", parameters)
            expected.update(payload=response, fits="yes" if model["fits"] else "no", maximum=f"{model['maximum_payload']} bytes")
        if scene.model == "resilience" and key == "options":
            parameters["options"] = values[key]
            model = experiment("resilience", parameters)
            expected[key] = response
        if spec.get("record"):
            expected[key] = response
        item = dict(id=f"post.{scene.id}.{key}", answer=expected[key],
                    type="hops" if key == "hops" else spec.get("type", "text"),
                    explanation=scene.explanation)
        checks[key] = learning.evaluate(item, response)
        if not checks[key]["format_valid"]:
            raise ValueError(checks[key]["feedback"])
    limits = ["Policy enforcement", "Return path and application response"] if scene.id.startswith("route.") else [
        "Claims beyond the declared scenario and supplied observation points",
        "Intent, unobserved paths and post-change service outcomes unless explicitly supplied"]
    result = dict(correct=all(c["correct"] for c in checks.values()), checks=checks,
                  explanation=scene.explanation, expected=expected,
                  unknowns=limits)
    if scene.model:
        result["model"] = model or experiment(scene.model, parameters)
        result["unknowns"] = result["model"]["unknowns"]
    return result


def fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [Path(__file__), Path(__file__).with_name("game.py"), ROOT / "learning.py", ROOT / "delivery.py"]
    paths += sorted(Path(__file__).with_name("assets").glob("*.json"))
    paths += sorted((ROOT / "modules").glob("*/workbench/*.py"))
    paths += sorted({source_path(c) for scene in scenes().values() for c in scene.cards})
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()
