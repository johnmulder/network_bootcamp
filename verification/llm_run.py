"""Durable bounded evaluation runs. A pending attempt is never resent automatically."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import time

import delivery as d
import llm

LIMITS = {"probe": 2, "baseline": 32, "candidate": 32, "held-out": 80, "session": 38, "diagnostic": 16}


def location(name):
    if not d.ID.fullmatch(name):
        raise ValueError("Use a simple run name with lowercase letters, digits, dots or hyphens")
    return d.session_file(d.session_dir("llm-evals"), name)


def create(name, server_info=""):
    cases = d.module_at("verification/llm_cases.py")
    coverage = cases.check()
    directory = location(name)
    directory.mkdir(parents=True, exist_ok=False)
    inventory = cases.cases()
    state = dict(created_at=d.now(), limits=LIMITS, coverage=coverage, server_info=server_info,
                 cases=inventory, cases_sha256=d.hash_text(llm.json_text(inventory)), stages={}, attempts=[],
                 criteria="Judge grounding, technical accuracy, false criticism, useful next steps, answer leakage, and responsiveness separately from output validity. Target at most 60 seconds per request. Agent judgments are not facilitator or learner validation.")
    d.save_state(directory, state)
    return dict(output=str(directory / "session.json"), **coverage, max_calls=sum(LIMITS.values()))


class Run:
    def __init__(self, name, stage, config, revision=""):
        self.directory, self.stage, self.config = location(name), stage, config
        if stage not in LIMITS:
            raise ValueError("Unknown evaluation stage")
        self.profile = dict(configuration=config.public(), prompt_version=llm.PROMPT_VERSION,
                            prompts=llm.PROMPTS, revision=revision,
                            runtime_sha256=d.hash_text((d.ROOT / "llm.py").read_text()))

    def load(self):
        state = d.decode_json(d.session_file(self.directory, "session.json").read_text())
        if state["limits"] != LIMITS or state["cases_sha256"] != d.hash_text(llm.json_text(state["cases"])):
            raise ValueError("The frozen run inventory or limits changed")
        return state

    def call(self, ident, feature, context, expectation="", metadata=None, generate=None):
        """Commit attempt before inference; only explicit replay returns cached results."""
        with d.session_lock(self.directory):
            state = self.load()
            prior_profile = state["stages"].get(self.stage)
            if prior_profile is not None and prior_profile != self.profile:
                raise ValueError("This stage's frozen configuration, prompts, or revision changed; use a new explicitly budgeted stage")
            state["stages"][self.stage] = self.profile
            key = self.stage + ":" + ident
            digest = d.hash_text(llm.json_text(dict(feature=feature, context=context)))
            old = next((a for a in state["attempts"] if a["key"] == key), None)
            if old:
                if old["context_sha256"] != digest:
                    raise ValueError("A recorded case's input changed")
                if old["status"] == "pending":
                    raise ValueError("Uncertain prior attempt; it is counted and will not be resent. Inspect it explicitly.")
                return copy.deepcopy(old)
            if len(state["attempts"]) >= sum(LIMITS.values()) or sum(a["stage"] == self.stage for a in state["attempts"]) >= LIMITS[self.stage]:
                raise ValueError("Evaluation call budget exhausted")
            _, size = llm.prepare_request(self.config, feature, context)
            entry = dict(key=key, stage=self.stage, feature=feature, status="pending", at=d.now(),
                         context_sha256=digest, context=context, input_bytes=size,
                         expectation=expectation, metadata=metadata or {}, facilitator_review=None)
            state["attempts"].append(entry)
            d.save_state(self.directory, state)
            started = time.monotonic()
            try:
                entry["output"] = (generate or llm.generate)(self.config, feature, context)
                entry["status"] = "accepted"
            except llm.LLMError as error:
                entry.update(status="rejected", error=str(error), code=error.code)
            entry.update(finished_at=d.now(), elapsed_ms=round((time.monotonic() - started) * 1000))
            d.save_state(self.directory, state)
            print(f"{key}: {entry['status']} ({entry['elapsed_ms']} ms)", flush=True)
            return copy.deepcopy(entry)


def batch(name, stage, count=80, resume=False, revision=""):
    if type(count) is not int or not 1 <= count <= 80:
        raise ValueError("A batch allows 1–80 attempted calls")
    run = Run(name, stage, llm.configuration(), revision)
    state = run.load()
    existing = [a for a in state["attempts"] if a["stage"] == stage]
    if existing and not resume:
        raise ValueError("Stage already has attempts; use explicit --resume")
    if stage == "probe":
        selected = [dict(id=name, feature="check", context={}, expectation="Return ready true.")
                    for name in ("connection", "connection-confirmation")]
    elif stage in ("baseline", "candidate", "held-out"):
        selected = [c for c in state["cases"] if c["split"] == ("held-out" if stage == "held-out" else "calibration")]
    else:
        raise ValueError("Use the session runner or explicit diagnostic calls for this stage")
    completed = {a["key"] for a in existing}
    sent = 0
    cases = d.module_at("verification/llm_cases.py")
    for case in selected:
        key = stage + ":" + case["id"]
        if key in completed:
            continue
        context = copy.deepcopy(case["context"])
        if case.get("turn", 0):
            current = run.load()
            previous = [a for a in current["attempts"] if a["stage"] == stage and a["metadata"].get("exchange_id") == case["exchange_id"]]
            if len(previous) != case["turn"] or any(a["status"] != "accepted" for a in previous):
                print(f"{key}: blocked by an unavailable previous turn", flush=True)
                continue
            context["exchange"] = [dict(reply=a["context"].get("reply", ""), advice=a["output"]["advice"]) for a in previous]
            context["reply"] = cases.learner_reply(previous[-1]["output"]["advice"]["question"], case["case"], case["reply_kind"])
        entry = run.call(case["id"], case["feature"], context, case["expectation"],
                         {k: v for k, v in case.items() if k not in ("context", "expectation")})
        sent += 1
        if entry["status"] == "rejected" or sent >= count:
            # Inspect each failure before explicitly resuming the remaining batch.
            break
    final = run.load()
    return dict(attempted_this_batch=sent, attempted_total=len(final["attempts"]),
                accepted=sum(a["status"] == "accepted" for a in final["attempts"]),
                pending=sum(a["status"] == "pending" for a in final["attempts"]),
                output=str(run.directory / "session.json"))


def session(name, filename, case="A", extended=False, resume=False, revision=""):
    from unittest import mock
    run = Run(name, "session", llm.configuration(), revision)
    if not resume and any(a["stage"] == "session" and a["key"].startswith("session:" + case + "-") for a in run.load()["attempts"]):
        raise ValueError("This session has prior attempts; use explicit --resume")
    original, index = llm.generate, 0
    def generate(config, feature, context):
        nonlocal index
        index += 1
        result = run.call(f"{case}-{index:02}-{feature}", feature, context,
                          "Useful feedback on authored partial work; reply responsiveness, no fabricated evidence or answer replacement.",
                          dict(case=case, phase=context["phase"]), generate=original)
        if result["status"] != "accepted":
            raise llm.LLMError(result["error"], result["code"])
        return result["output"]
    with mock.patch.object(llm, "generate", side_effect=generate):
        return d.module_at("verification/check_llm.py").evaluate_session(filename, run.load()["server_info"], case, extended)
