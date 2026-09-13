"""Session-bound advisory actions; the model has no course or filesystem tools."""

from __future__ import annotations

import copy
import json

import delivery as d
import llm

STATUSES = {"pending", "complete", "failed", "stale", "cancelled"}
REVIEW_SUBMISSIONS = {"c01": "c01.change", "c02": "c02.calculate", "c03": "c03.compare",
                      "c04": "c04.twist", "c05": "c05.narrative", "c06": "c06.handoff"}


def actions(phase: dict) -> list[str]:
    features = llm.availability()["features"]
    if phase["block"] == "exit":
        return []
    result = []
    if "review" in features and phase["kind"] == "review" and phase["block"] in REVIEW_SUBMISSIONS:
        result.append("llm_review")
    if "coach" in features and any(b["role"] == "conceptual" for b in phase["assessment"].values()):
        result.append("llm_coach")
    if "handoff" in features and phase["id"] == "c06.exchange":
        result.append("llm_handoff")
    return result


def public_history(state: dict) -> list[dict]:
    keys = ("id", "phase", "feature", "status", "at", "finished_at", "context_sha256",
            "artifact_hashes", "model", "endpoint", "prompt_version", "source_ids",
            "latency_ms", "usage", "error_code", "response_format")
    return [{k: copy.deepcopy(entry[k]) for k in keys if k in entry} for entry in state["llm_requests"].values()]


def validate_state(state: dict) -> None:
    records = state["llm_requests"]
    if not isinstance(records, dict):
        raise ValueError("Invalid LLM history")
    for ident, entry in records.items():
        if (not isinstance(entry, dict) or not d.ID.fullmatch(ident) or entry["id"] != ident
                or entry["phase"] not in state["phases"] or entry["status"] not in STATUSES
                or entry["feature"] not in {"review", "coach", "handoff"}
                or entry["request"]["request_id"] != ident
                or entry["request"]["action"] != "llm_" + entry["feature"]
                or not isinstance(entry["context"], dict)
                or not isinstance(entry["artifact_hashes"], dict)
                or type(entry["prepared_revision"]) is not int):
            raise ValueError("Invalid LLM request record")
        if entry["context_sha256"] != context_hash(entry["context"]):
            raise ValueError("LLM context changed")
        if entry["status"] == "complete":
            try:
                llm.validate_output(entry["feature"], entry["advice"], entry["context"])
            except llm.LLMError:
                raise ValueError("Invalid saved advice") from None


def context_hash(context: dict) -> str:
    return d.hash_text(json.dumps(context, sort_keys=True, ensure_ascii=False, allow_nan=False))


def opened_evidence(state: dict, data: dict, phase: dict) -> dict:
    """Use recorded command output, never expand a partial view to its source."""
    evidence = {}
    limit = state["order"].index(phase["id"])
    mapping = d.workbench(1).read_json("challenges/evidence-map.json")
    for saved in state["requests"].values():
        request = saved["request"]
        if request["action"] != "evidence":
            continue
        source_phase = d.phase_by_id(data, request["phase_id"])
        view = request["payload"]["view"]
        if (source_phase["block"] != phase["block"] or state["order"].index(source_phase["id"]) > limit
                or view not in state["phases"][source_phase["id"]]["views"] or view.startswith("case.exit")):
            continue
        result = saved["response"]["result"]
        output = result["output"]["stdout"]
        evidence["view:" + view] = dict(text=output, view=view,
                                       note="Saved view; derived copies are not independent sensors.")
        if view.startswith("incident.round"):
            round_id = view.removeprefix("incident.round")
            packet = d.decode_json(output)
            for source in mapping["incident_rounds"][round_id]:
                if source not in packet or not source.endswith(".jsonl"):
                    continue
                originals = d.workbench(3).read_jsonl(source)
                for record in packet[source]:
                    # Only exact records already displayed receive original IDs.
                    matches = [i for i, original in enumerate(originals, 1) if original == record]
                    if len(matches) == 1:
                        evidence[f"{source}#{matches[0]}"] = dict(record=record, source=source, derived_view=view)
        elif view in ("case.main", "case.main.observations"):
            packet = d.decode_json(output)
            for record in packet["observations"]:
                evidence[record["id"]] = dict(record=record, source=f"challenges/case-{state['case'].lower()}.json", derived_view=view)
    return evidence


def build_context(state: dict, data: dict, phase: dict, feature: str, payload: dict) -> tuple[dict, dict]:
    directory = d.session_dir(state["id"])
    progress = state["phases"][phase["id"]]
    if phase["block"] == "exit":
        raise d.DeliveryError("LLM advice is unavailable for the independent exit", 3)
    evidence = opened_evidence(state, data, phase)
    context = dict(phase=phase["id"], evidence=evidence,
                   limitation="Only opened views are supplied. Missing coverage and intent remain unknown.")
    hashes = d.review_hashes(directory, phase)
    if feature == "coach":
        if set(payload) != {"family"}:
            raise d.DeliveryError("Coaching needs exactly a family")
        family = payload["family"]
        checks = [name for name, b in phase["assessment"].items() if b["role"] == "conceptual" and b["family"] == family]
        submissions = [s for s in progress["submissions"] if any(k in s["checks"] for k in checks)]
        if not checks or not submissions:
            raise d.DeliveryError("Commit an answer for this phase's selected family before coaching", 3)
        latest = submissions[-1]
        context.update(family=family, learner_text=latest["text"],
                       questions=[d.public_checkpoint(q) for q in d.checkpoint_items(phase, state) if q["id"] in checks],
                       answers={k: v for k, v in latest["answers"].items() if k in checks},
                       results={k: v for k, v in latest["checks"].items() if k in checks})
    else:
        if feature == "review" and payload:
            raise d.DeliveryError("LLM review takes an empty payload")
        if feature == "handoff" and (set(payload) - {"role", "text"} or payload.get("role") not in llm.ROLES):
            raise d.DeliveryError("Handoff needs a listed role and optional text")
        required = REVIEW_SUBMISSIONS.get(phase["block"])
        if not required or not state["phases"][required]["submissions"]:
            raise d.DeliveryError("Submit the block's explanation before requesting advice", 3)
        if phase["block"] == "c06" and ("diagnosis" not in state["phases"]["c06.receive"]
                                         or not state["phases"]["c06.analyze"]["submissions"]):
            raise d.DeliveryError("Record the initial diagnosis and investigation first", 3)
        assessment_phase = d.phase_by_id(data, phase["block"] + ".review")
        check = d.validate_artifacts(directory, assessment_phase, state)
        if not check["valid"]:
            raise d.DeliveryError("Complete the artifact structure and references before LLM review", 3, check)
        dependencies = d.review_dependencies(directory, phase)
        regions = {k: v for k, v in dependencies.items() if not k.startswith("evidence-ledger.csv#")}
        ledger = {k.removeprefix("evidence-ledger.csv#"): v for k, v in dependencies.items()
                  if k.startswith("evidence-ledger.csv#") and k != "evidence-ledger.csv#header"}
        if any(ident not in evidence for ident in ledger):
            raise d.DeliveryError("Open the evidence views for all cited ledger records before requesting advice", 3)
        context.update(learner_text="\n\n".join(regions.values()), regions=regions,
                       ledger=ledger, rubric=d.REVIEW_GUIDE)
        if feature == "handoff":
            # The snapshot, not role choice or wording, defines the three-turn limit.
            snapshot = context_hash(dict(regions=regions, ledger=ledger))
            previous = [r for r in state["llm_requests"].values()
                        if r["feature"] == "handoff" and r["status"] == "complete"
                        and r["context"].get("handoff_snapshot") == snapshot]
            if len(previous) >= 3:
                raise d.DeliveryError("This handoff has three model turns; revise it or use the rubric", 3)
            text = payload.get("text", "")
            if not isinstance(text, str):
                raise d.DeliveryError("Handoff reply must be text")
            if text:
                d.require_text(text)
            if previous and not text:
                raise d.DeliveryError("Answer the previous recipient question before the next turn")
            context.update(role=payload["role"], handoff_snapshot=snapshot, reply=text,
                           exchange=[dict(reply=r["context"].get("reply", ""), advice=r["advice"])
                                     for r in previous])
    # Only this phase's teaching fragment, never a linked solution or future brief.
    if feature != "coach":
        context["instructions"] = d.render_references(phase["content"], state)
    if len(json.dumps(context, ensure_ascii=False).encode()) > llm.CONTEXT_LIMIT:
        raise d.DeliveryError("Selected context exceeds 64 KiB; use static support for this submission")
    return context, hashes


def expose(state: dict, data: dict, phase: dict, feature: str, payload: dict) -> None:
    for peer in data["phases"]:
        if (feature == "coach" and peer["id"] != phase["id"]) or peer["block"] != phase["block"]:
            continue
        family = payload["family"] if feature == "coach" else None
        d.expose_checks(state["phases"][peer["id"]], peer, family)
        for assigned in state["learning"]:
            if assigned["phase"] == peer["id"] and (family is None or assigned["family"] == family) and not assigned["responses"]:
                assigned["exposed"] = True
                assigned.setdefault("help", []).append(dict(at=d.now(), kind="llm:" + feature))
    state["phases"][phase["id"]].setdefault("help_history", []).append(dict(at=d.now(), kind="llm:" + feature))


def response_for(state: dict, data: dict, entry: dict) -> dict:
    result = dict(action="llm_" + entry["feature"], phase_id=entry["phase"],
                  learning_result="advisory_" + entry["status"], llm_request_id=entry["id"])
    if entry["status"] == "complete":
        result["advice"] = copy.deepcopy(entry["advice"])
        result["notice"] = "Advisory model feedback; recorded as answer-bearing help. Human review determines rubric scores."
    elif entry["status"] == "pending":
        result["notice"] = "Request pending. No additional inference was sent; wait or explicitly cancel it before retrying."
    else:
        result["notice"] = entry.get("error", "Advice was not delivered; use existing hints or rubric.")
    return d.status_result(state, data, result, view_phase=entry["phase"])


def act(ident: str, request: dict) -> dict:
    """Reserve once, infer outside the lock, persist exposure before delivery."""
    data, directory = d.definition(), d.session_dir(ident)
    with d.session_lock(directory):
        state = d.load_state(directory, data)
        old = state["requests"].get(request["request_id"])
        entry = state["llm_requests"].get(request["request_id"])
        if old or entry:
            if (old or entry)["request"] != request:
                raise d.DeliveryError("Request ID was already used for different input", 3)
            return old["response"] if old else response_for(state, data, entry)
        if request["expected_revision"] != state["revision"]:
            raise d.DeliveryError("Stale session revision; fetch status before requesting advice", 3)
        phase = d.phase_by_id(data, request["phase_id"])
        limit = state["order"].index(state["current"]) if state["current"] else len(state["order"])
        if state["order"].index(phase["id"]) > limit:
            raise d.DeliveryError("This phase has not been released yet", 3)
        if request["action"] == "llm_cancel":
            if set(request["payload"]) != {"request_id"} or not isinstance(request["payload"]["request_id"], str):
                raise d.DeliveryError("Cancellation needs the pending request_id")
            entry = state["llm_requests"].get(request["payload"]["request_id"])
            if not entry or entry["status"] != "pending":
                raise d.DeliveryError("Choose a pending LLM request", 3)
            entry.update(status="cancelled", finished_at=d.now())
            state["revision"] += 1
            state["updated_at"] = d.now()
            result = response_for(state, data, entry)
            state["requests"][request["request_id"]] = dict(request=request, response=result)
            d.save_state(directory, state)
            return result
        if request["action"] not in actions(phase):
            raise d.DeliveryError("LLM action is disabled, misconfigured, or unavailable in this phase", 3)
        if any(r["status"] == "pending" for r in state["llm_requests"].values()):
            raise d.DeliveryError("An LLM request is pending; wait or cancel it before requesting another", 3)
        feature = request["action"].removeprefix("llm_")
        config = llm.configuration()
        context, hashes = build_context(state, data, phase, feature, request["payload"])
        state["revision"] += 1
        state["updated_at"] = d.now()
        entry = dict(id=request["request_id"], request=copy.deepcopy(request), phase=phase["id"], feature=feature,
                     status="pending", at=d.now(), context=context, context_sha256=context_hash(context),
                     artifact_hashes=hashes, prepared_revision=state["revision"], source_ids=sorted(context["evidence"]),
                     model=config.model, endpoint=config.base_url, prompt_version=llm.PROMPT_VERSION,
                     response_format=config.response_format)
        state["llm_requests"][entry["id"]] = entry
        d.save_state(directory, state)
    try:
        generated, failure = llm.generate(config, feature, context), None
    except llm.LLMError as error:
        generated, failure = None, error
    with d.session_lock(directory):
        state = d.load_state(directory, data)
        entry = state["llm_requests"][request["request_id"]]
        if entry["status"] != "pending":
            return response_for(state, data, entry)
        before_advice = copy.deepcopy(state)
        stale = state["revision"] != entry["prepared_revision"] or d.review_hashes(directory, phase) != entry["artifact_hashes"]
        if stale:
            entry.update(status="stale", error="Work changed while advice was generated; no advice was delivered.")
        elif failure:
            entry.update(status="failed", error=str(failure), error_code=failure.code)
        else:
            entry.update(status="complete", **generated)
            expose(state, data, phase, feature, request["payload"])
        entry["finished_at"] = d.now()
        state["revision"] += 1
        state["updated_at"] = d.now()
        response = response_for(state, data, entry)
        if entry["status"] == "complete" and d.review_hashes(directory, phase) != entry["artifact_hashes"]:
            state = before_advice
            entry = state["llm_requests"][request["request_id"]]
            entry.update(status="stale", finished_at=d.now(), error="Assessed work changed during commit; advice discarded.")
            state["revision"] += 1
            state["updated_at"] = d.now()
            response = response_for(state, data, entry)
        state["requests"][entry["id"]] = dict(request=request, response=response)
        d.save_state(directory, state)
        return response
