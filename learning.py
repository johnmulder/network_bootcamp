"""Finite authored practice and factual scoring; no prose grading or live network I/O."""

from __future__ import annotations

import hashlib
import ipaddress
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

CATALOG = Path(__file__).resolve().parent / "delivery/problems.json"


def catalog() -> dict:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data["version"] != 1:
        raise ValueError("Unsupported problem catalog")
    seen = set()
    for family, items in data["families"].items():
        if sum(p["use"] == "reassessment" for p in items) < 2 or not any(p["use"] == "supported" for p in items):
            raise ValueError(f"Family needs supported practice and two fresh variants: {family}")
        fields = None
        for problem in items:
            if problem["id"] in seen or problem["family"] != family or not problem["provenance"]:
                raise ValueError("Invalid or duplicate problem")
            seen.add(problem["id"])
            current = {q["id"] for q in problem["questions"]}
            if not current or (fields is not None and fields != current):
                raise ValueError("Variants must assess the same fields")
            fields = current
            for question in problem["questions"]:
                if not evaluate(question, question["answer"])["correct"]:
                    raise ValueError(f"Invalid authored answer: {problem['id']}")
            if family == "transfer":
                p = problem["parameters"]
                if not (0 < p["ipv4_header"] + p["tcp_header"] < p["mtu"] <= 9000):
                    raise ValueError("Invalid transfer bounds")
                if problem["questions"][0]["answer"] != f"{p['mtu'] - p['ipv4_header'] - p['tcp_header']} bytes":
                    raise ValueError("Transfer key differs from declared conditions")
    return data


def normalize(text: str) -> str:
    return " ".join(text.strip().rstrip(".").lower().replace(",", " ").replace("->", " ").split())


def evaluate(item: dict, response: str) -> dict:
    """Semantic equality for bounded facts; recognize only explicitly known errors."""
    if not isinstance(response, str) or not response.strip() or len(response) > 16000:
        raise ValueError("Answer must be nonempty text of at most 16000 characters")
    answer, expected = response.strip(), str(item["answer"])
    kind = item.get("type", "text")
    ident = item["id"]
    if ident == "transfer.payload":
        kind = "bytes"
    elif ident == "m1.convergence.interval":
        kind = "milliseconds"
    elif ident.startswith("route.") and ident.endswith("hops"):
        kind = "hops"
    elif ident == "incident.utc":
        kind = "utc"
    if kind == "text":
        try:
            ipaddress.ip_network(expected)
            kind = "prefix" if "/" in expected else "ip"
        except ValueError:
            pass
    valid, code = True, "unclassified"
    correct = normalize(answer) in {normalize(str(a)) for a in item.get("answers", [expected])}
    try:
        if kind in ("bytes", "milliseconds"):
            match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)\s*([A-Za-z]+)?", answer)
            if not match:
                raise ValueError("quantity")
            number, unit = float(match[1]), match[2] or ""
            if kind == "bytes":
                if not unit:
                    raise ValueError("Include bytes or bits")
                target = float(expected.split()[0])
                # Preserve case: B means bytes; b means bits.
                byte_unit = unit == "B" or unit.lower() in ("byte", "bytes")
                bit_unit = unit == "b" or unit.lower() in ("bit", "bits")
                if not byte_unit and not bit_unit:
                    raise ValueError("Use bytes or bits")
                correct = number == target and byte_unit
                headers = item.get("headers", [20, 20])
                if not byte_unit:
                    code = "wrong-units"
                elif number == target + sum(headers):
                    code = "missing-both-headers"
                elif number in {target + h for h in headers}:
                    code = "missing-one-header"
            else:
                if unit.lower() not in ("", "ms", "milliseconds", "s", "seconds"):
                    raise ValueError("Use milliseconds or seconds")
                correct = number * (1000 if unit.lower() in ("s", "seconds") else 1) == float(expected.split()[0])
        elif kind == "hops":
            actual = [str(ipaddress.ip_address(p.strip())) for p in answer.split(",")]
            wanted = {str(ipaddress.ip_address(p.strip())) for p in expected.split(",")}
            correct = len(actual) == len(set(actual)) and set(actual) == wanted
        elif kind in ("prefix", "ip"):
            parse = ipaddress.ip_network if kind == "prefix" else ipaddress.ip_address
            correct = False if normalize(answer) in ("no route", "none") else parse(answer) == parse(expected)
        elif kind == "utc":
            actual = datetime.fromisoformat(answer.replace("Z", "+00:00"))
            target = datetime.fromisoformat(expected.replace("Z", "+00:00"))
            if actual.tzinfo is None:
                raise ValueError("Include UTC zone")
            correct = actual == target and actual.utcoffset() == timedelta(0)
            local = datetime.fromisoformat(item.get("local_time", "2026-08-15T10:04:01-06:00"))
            if actual == target + 2 * local.utcoffset():
                code = "utc-direction"
    except (ValueError, TypeError):
        valid, correct, code = False, False, "input-format"
    if not correct and valid:
        common = {
            "m1.routes.10.0.20.40": [("10.0.0.0/8", "prefix-before-preference"), ("10.0.20.0/24", "prefix-before-preference"), ("0.0.0.0/0", "prefix-before-preference")],
            "m1.convergence.application": [("yes", "application-not-observed")],
            "opening.application": [("yes", "application-not-observed")],
            "flows.server-ot": [("enforced", "intent-not-enforcement"), ("proven", "intent-not-enforcement")],
            "flows.user-ot": [("enforced", "intent-not-enforcement"), ("proven", "intent-not-enforcement")],
        }
        for value, category in common.get(ident, []):
            if normalize(answer) == value:
                code = category
        for rule in item.get("misconceptions", []):
            if normalize(answer) in {normalize(a) for a in rule["answers"]}:
                code = rule["code"]
    messages = {
        "wrong-units": "Keep bits and bytes distinct. The path limit and headers are measured in bytes.",
        "missing-both-headers": "The MTU bounds the whole IP packet. Which two headers occupy space inside it?",
        "missing-one-header": "Account for both the IP and TCP headers; inspect ip.hdr_len and tcp.hdr_len.",
        "prefix-before-preference": "Select the longest matching prefix before comparing route preference among equal prefixes.",
        "application-not-observed": "Control-plane or transport progress alone does not show application recovery. What application observation is missing?",
        "intent-not-enforcement": "An intended policy decision is not a measured enforcement result. Inspect the intended field and identify the missing observation.",
        "utc-direction": "A negative offset means local time is behind UTC. Move forward by the stated offset magnitude.",
        "input-format": "Use the factual format requested by the prompt; this input did not consume an attempt.",
    }
    if correct:
        code, feedback = "correct", item.get("explanation", "Correct.")
    else:
        feedback = messages.get(code, "This answer does not match the supplied evidence. Reinspect the named fields and explain your selection rule.")
    return dict(id=ident, correct=correct, format_valid=valid, feedback_code=code,
                feedback=feedback, evidence=item.get("evidence", "declared problem conditions"))


def public_problem(problem: dict) -> dict:
    return {**{key: problem[key] for key in ("id", "family", "parameters", "provenance", "prompt", "use")},
            "questions": [{key: q[key] for key in ("id", "prompt")} for q in problem["questions"]]}


def assignments(state: dict) -> list[dict]:
    return state.setdefault("learning", [])


def find_problem(variant_id: str) -> dict:
    for variants in catalog()["families"].values():
        for problem in variants:
            if problem["id"] == variant_id:
                return problem
    raise ValueError("Unknown problem variant")


def assign(state: dict, phase: dict, family: str, use: str, at: str) -> dict:
    bindings = [b for b in phase["assessment"].values() if b["family"] == family]
    if not bindings:
        raise ValueError("Choose a problem family attached to this checkpoint phase")
    attempts = assignments(state)
    for entry in attempts:
        if entry["phase"] == phase["id"] and entry["family"] == family and entry["use"] == use and not entry["responses"]:
            return public_problem(find_problem(entry["variant_id"]))
    used = {a["variant_id"] for a in attempts}
    variants = [p for p in catalog()["families"].get(family, []) if p["use"] == use and p["id"] not in used]
    if not variants:
        return dict(family=family, exhausted=True, message="No unseen variant remains. This objective stays unmet unless already satisfied.")
    variants.sort(key=lambda p: hashlib.sha256(f"{state['seed']}:{p['id']}".encode()).hexdigest())
    problem = variants[0]
    attempts.append(dict(variant_id=problem["id"], family=family, phase=phase["id"],
                         parameters=problem["parameters"], presented_at=at, use=use,
                         exposed=use != "reassessment", responses=[],
                         objectives={b["objective"]: b["field"] for b in bindings}))
    return public_problem(problem)


def problem_action(state: dict, phase: dict, action: str, payload: dict, at: str) -> dict:
    required = {"reassess": {"family"}, "support": {"family"}, "problem_hint": {"variant_id"},
                "problem_answer": {"variant_id", "answers"}}[action]
    optional = {"level"} if action == "support" else set()
    if not required <= set(payload) or set(payload) - required - optional:
        raise ValueError("Unexpected or missing learning action fields")
    if action in ("reassess", "support"):
        family = payload.get("family")
        if family not in {b["family"] for b in phase["assessment"].values() if b["role"] == "conceptual"}:
            raise ValueError("Select a conceptual family shown for this phase")
        if action == "support" and payload.get("level", "practice") == "orientation":
            return dict(orientation="Read the declared conditions, identify the governing rule, and include the requested units. You may answer directly or choose supported practice.")
        if action == "support" and payload.get("level", "practice") not in ("practice", "worked"):
            raise ValueError("Support level must be orientation, practice, or worked")
        result = assign(state, phase, family, "reassessment" if action == "reassess" else "supported", at)
        if action == "support" and payload.get("level") == "worked" and "id" in result:
            entry = next(a for a in assignments(state) if a["variant_id"] == result["id"])
            entry["exposed"] = True
            entry.setdefault("help", []).append(dict(at=at, kind="worked"))
            result["worked"] = find_problem(result["id"])["questions"]
        return result
    entry = next((a for a in assignments(state) if a["variant_id"] == payload.get("variant_id") and a["phase"] == phase["id"]), None)
    if entry is None:
        raise ValueError("Use a problem already assigned in this phase")
    problem = find_problem(entry["variant_id"])
    if action == "problem_hint":
        entry["exposed"] = True
        entry.setdefault("help", []).append(dict(at=at, kind="answer-bearing"))
        return dict(worked=problem["questions"], independent=False)
    answers = payload.get("answers")
    if not isinstance(answers, dict) or set(answers) != {q["id"] for q in problem["questions"]}:
        raise ValueError("Supply exactly the assigned problem's answer IDs")
    results = {q["id"]: evaluate(q, answers[q["id"]]) for q in problem["questions"]}
    if not all(r["format_valid"] for r in results.values()):
        raise ValueError("Invalid factual format; attempt unchanged. Include the requested units and field formats.")
    independent = not entry["exposed"] and not entry["responses"] and entry["use"] == "reassessment"
    record = dict(at=at, answers=answers, results=results, independent=independent,
                  passed=all(r["correct"] for r in results.values()))
    entry["responses"].append(record)
    return dict(results=results, independent=independent and record["passed"],
                learning_result="reassessed" if independent and record["passed"] else "practice")


def attained(state: dict, objective: str) -> bool:
    return any(objective in a["objectives"] and any(r["independent"] and r["passed"] for r in a["responses"])
               for a in state.get("learning", []))


EXPERIMENT_VERSION = 1
EXPERIMENT_CHOICES = {
    "transfer": {"scenario": ["plain", "tcp-options", "ip-options"], "payload": [128, 1144, 1160, 1161, 1400]},
    "routing": {"condition": ["baseline", "remove-host-route", "CORP", "OT"], "destination": ["10.0.20.40", "198.51.100.77"]},
    "resilience": {"options": ["state-sync", "backup-path", "monitoring", "management"],
                   "failure": ["session-sync-stale", "20-percent-loss", "power-loss", "stale-answer"], "twist": [False, True]},
}


def experiment(model: str, parameters: dict, baseline: dict, select_routes=None, best_vrf_route=None) -> dict:
    """Evaluate a finite decision model against supplied immutable baseline data."""
    if model not in EXPERIMENT_CHOICES or not isinstance(parameters, dict) or set(parameters) != set(EXPERIMENT_CHOICES[model]):
        raise ValueError("Use exactly the displayed experiment parameters")
    for key, values in EXPERIMENT_CHOICES[model].items():
        value = parameters[key]
        if key == "options":
            if not isinstance(value, list) or len(value) != 2 or any(not isinstance(v, str) for v in value) or len(set(value)) != 2 or any(v not in values for v in value):
                raise ValueError("Choose two distinct listed improvements")
        elif type(value) is not type(values[0]) or value not in values:
            raise ValueError(f"Choose a listed {key}")
    if model == "transfer":
        ip, tcp = {"plain": (20, 20), "tcp-options": (20, 32), "ip-options": (24, 32)}[parameters["scenario"]]
        mtu = baseline["mtu"]
        payload = parameters["payload"]
        return dict(mtu=mtu, ipv4_header=ip, tcp_header=tcp, maximum_payload=mtu-ip-tcp,
                    packet_bytes=payload+ip+tcp, fits=payload+ip+tcp <= mtu,
                    unknowns=["Delivery of ICMP feedback", "Application retry behavior and recovery"])
    if model == "routing":
        destination, condition = parameters["destination"], parameters["condition"]
        if condition in ("CORP", "OT"):
            route = best_vrf_route(condition, destination, baseline["vrfs"])
            routes = [route] if route else []
        else:
            rows = [r for r in baseline["routes"] if condition != "remove-host-route" or r["prefix"] != "10.0.20.40/32"]
            routes = select_routes(destination, rows)
        return dict(prefix=routes[0]["prefix"] if routes else "no route",
                    next_hops=sorted({r["next_hop"] for r in routes}),
                    unknowns=["Policy enforcement", "Return path and application response"])
    options = parameters["options"]
    condition = parameters["failure"]
    record = next(r for r in baseline["failures"] if r["condition"] == condition)
    addressed = []
    if "state-sync" in options and condition == "session-sync-stale":
        addressed.append("Selected state-sync work targets the recorded stale-state dependency; successful validation remains required.")
    if "backup-path" in options and condition == "20-percent-loss":
        addressed.append("A separately routed path is a candidate around impairment; its loss and spare capacity must be measured.")
    if "monitoring" in options:
        addressed.append("Service monitoring targets detection; measure polling and alert delay against the one-minute requirement.")
    if "management" in options:
        addressed.append("Management access targets diagnosis and recovery access; verify transport and power independence.")
    residual = ["No option establishes successful failover, application recovery, or policy enforcement without validation."]
    if condition in ("power-loss", "stale-answer"):
        residual.append("Neither chosen token repairs this recorded power or DNS failure directly.")
    if parameters["twist"]:
        residual.append("Both transport paths share building power and current management uses the preferred circuit; transport redundancy alone cannot survive the shared feed loss.")
    if not addressed:
        residual.append("The chosen improvements do not directly address this modeled failure condition.")
    return dict(baseline_affected=record["affected"], addressed_dependencies=addressed,
                residual_risk=residual, unknowns=["Post-change established-session survival", "New-connection success", "Backup capacity and independence"])
