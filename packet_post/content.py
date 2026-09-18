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


def choice(key, label, options, *, multiple=False):
    return dict(key=key, label=label, options=options, multiple=multiple)


def text_field(key, label, kind="text"):
    return dict(key=key, label=label, type=kind)


def card(ident, source, label, *, category="Declared condition", point="unknown", parents=()):
    return dict(id=ident, source=source, label=label, category=category,
                point=point, parents=list(parents))


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
    return result


def missions() -> list[dict]:
    return [dict(id="sorting", title="The Sorting Office", character="Pip & the prefix clerk",
        flavor="Small labels. Big opinions. Please sort the mail before the tea cools.",
        lesson="challenges/01-be-the-packet.md", duration="12-15 minutes",
        intro="In a separate worked example, destination 192.0.2.8 matches both 192.0.2.0/24 and "
              "192.0.2.8/32. The /32 is more specific. Our office chooses forwarding; it cannot promise "
              "a complete service path. Open evidence with E, then make your prediction.",
        steps=["route.host", "route.remove", "route.vrf", "route.limits"], stamp="Return Address Included")]


def mission(ident):
    return next(m for m in missions() if m["id"] == ident)


def evidence(item: dict) -> str:
    path = FIXTURES / item["source"]
    if path.suffix == ".json":
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
    for spec in scene.fields:
        key, response = spec["key"], values[spec["key"]]
        if spec.get("multiple"):
            if not isinstance(response, list) or not response or len(set(response)) != len(response):
                raise ValueError("Choose each eligible option once.")
            if any(v not in spec["options"] for v in response):
                raise ValueError("Choose displayed options.")
            response = ", ".join(response)
        elif not isinstance(response, str) or not response.strip() or len(response) > 1600:
            raise ValueError("Complete each field (up to 1600 characters).")
        if "options" in spec and not spec.get("multiple") and response not in spec["options"]:
            raise ValueError("Choose a displayed option.")
        item = dict(id=f"post.{scene.id}.{key}", answer=scene.expected[key],
                    type="hops" if key == "hops" else spec.get("type", "text"),
                    explanation=scene.explanation)
        checks[key] = learning.evaluate(item, response)
        if not checks[key]["format_valid"]:
            raise ValueError(checks[key]["feedback"])
    result = dict(correct=all(c["correct"] for c in checks.values()), checks=checks,
                  explanation=scene.explanation, expected=scene.expected,
                  unknowns=["Policy enforcement", "Return path and application response"])
    if scene.model:
        result["model"] = experiment(scene.model, scene.parameters)
        result["unknowns"] = result["model"]["unknowns"]
    return result


def fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [Path(__file__), Path(__file__).with_name("game.py"), ROOT / "learning.py"]
    paths += sorted((ROOT / "modules").glob("*/workbench/*.py"))
    paths += [FIXTURES / s for s in sorted({c["source"] for scene in scenes().values() for c in scene.cards})]
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()
