"""Authored decisions and small adapters to the existing course models."""

from __future__ import annotations

import hashlib
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


def choice(key, label, options, *, multiple=False, count=None):
    return dict(key=key, label=label, options=options, multiple=multiple, count=count)


def text_field(key, label, kind="text"):
    return dict(key=key, label=label, type=kind)


def card(ident, source, label, *, category="Declared condition", point="unknown", parents=(), projection=None):
    return dict(id=ident, source=source, label=label, category=category,
                point=point, parents=list(parents), projection=projection)


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
            [ROUTES], ROUTE_BOARD,
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
    result.update(parcel_scenes())
    result.update(resilience_scenes())
    return result


def parcel_scenes():
    result = {}
    capture = card("transfer", "challenges/transfer.pcap", "Frames 1-6 of the transfer drill",
                   category="Recorded observation", parents=("challenges/transfer.pcap",), projection="transfer")
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
    return [dict(id="sorting", title="The Sorting Office", character="Pip & the prefix clerk",
        flavor="Small labels. Big opinions. Please sort the mail before the tea cools.",
        lesson="challenges/01-be-the-packet.md", duration="12-15 minutes",
        intro="In a separate worked example, destination 192.0.2.8 matches both 192.0.2.0/24 and "
              "192.0.2.8/32. The /32 is more specific. Our office chooses forwarding; it cannot promise "
              "a complete service path. Open evidence with E, then make your prediction.",
        steps=["route.host", "route.remove", "route.vrf", "route.limits"], stamp="Return Address Included"),
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


def mission(ident):
    return next(m for m in missions() if m["id"] == ident)


def evidence(item: dict) -> str:
    path = FIXTURES / item["source"]
    if item.get("projection"):
        projection = json.loads((Path(__file__).with_name("assets") / "observations.json").read_text())[item["projection"]]
        if hashlib.sha256(path.read_bytes()).hexdigest() != projection["sha256"]:
            raise ValueError("Decoded observation is stale; restore its matching source capture.")
        body = json.dumps(projection, indent=2)
    elif path.suffix == ".json":
        body = json.dumps(json.loads(path.read_text()), indent=2)
    else:
        body = path.read_text().strip()
    return (f"{item['category']} | {item['label']}\nScenario/source: labs/fixtures/{item['source']}\n"
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
            if not isinstance(response, list) or not response or len(set(response)) != len(response):
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
        item = dict(id=f"post.{scene.id}.{key}", answer=expected[key],
                    type="hops" if key == "hops" else spec.get("type", "text"),
                    explanation=scene.explanation)
        checks[key] = learning.evaluate(item, response)
        if not checks[key]["format_valid"]:
            raise ValueError(checks[key]["feedback"])
    result = dict(correct=all(c["correct"] for c in checks.values()), checks=checks,
                  explanation=scene.explanation, expected=expected,
                  unknowns=["Policy enforcement", "Return path and application response"])
    if scene.model:
        result["model"] = model or experiment(scene.model, parameters)
        result["unknowns"] = result["model"]["unknowns"]
    return result


def fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [Path(__file__), Path(__file__).with_name("game.py"), ROOT / "learning.py"]
    paths += sorted(Path(__file__).with_name("assets").glob("*.json"))
    paths += sorted((ROOT / "modules").glob("*/workbench/*.py"))
    paths += [FIXTURES / s for s in sorted({c["source"] for scene in scenes().values() for c in scene.cards})]
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()
