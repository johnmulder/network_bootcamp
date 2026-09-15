"""Learning contracts and independent checks of authored problems."""

import json
import csv
import ipaddress
import unittest
import contextlib
import io
from concurrent.futures import ThreadPoolExecutor
from unittest import mock
from pathlib import Path

import delivery as d
import learning
import test_delivery as journeys

ROOT = Path(__file__).resolve().parents[1]


class LearningContractTests(unittest.TestCase):
    def test_every_checkpoint_has_an_explicit_assessment_role(self):
        course = json.loads((ROOT / "delivery/course.json").read_text())
        objectives = []
        occurrences = 0
        for phase in course["phases"]:
            self.assertEqual(set(phase["checkpoints"]), set(phase["assessment"]))
            for check, binding in phase["assessment"].items():
                occurrences += 1
                if check in {"case.id", "budget.options", "incident.auth-record"}:
                    self.assertEqual(binding["role"], "recording")
                    self.assertIsNone(binding["objective"])
                else:
                    self.assertEqual(binding["role"], "conceptual")
                    self.assertIn(binding["family"], course["learning_contract"]["families"])
                    self.assertEqual(binding["support"], binding["family"])
                    self.assertTrue(binding["field"])
                    objectives.append(binding["objective"])
        self.assertEqual(occurrences, 29)
        self.assertEqual(len(objectives), 25)
        self.assertEqual(len(set(objectives)), len(objectives))

    def test_semantic_quantities_and_misconceptions(self):
        item = dict(id="transfer.payload", answer="1160 bytes", evidence="ip.hdr_len and tcp.hdr_len")
        for answer in ("1160 bytes", "1160 B", "1160.0 Bytes"):
            self.assertTrue(learning.evaluate(item, answer)["correct"])
        for answer, code in (("1160 b", "wrong-units"), ("1160 bits", "wrong-units"),
                             ("1200 bytes", "missing-both-headers"), ("1180 bytes", "missing-one-header")):
            result = learning.evaluate(item, answer)
            self.assertFalse(result["correct"])
            self.assertEqual(result["feedback_code"], code)
        self.assertFalse(learning.evaluate(item, "1160")["format_valid"])
        hops = dict(id="route.after-hops", answer="10.0.0.1, 10.0.0.2")
        self.assertTrue(learning.evaluate(hops, "10.0.0.2,10.0.0.1")["correct"])
        self.assertFalse(learning.evaluate(hops, "10.0.0.1,10.0.0.1,10.0.0.2")["correct"])
        time = dict(id="m1.convergence.interval", answer="80")
        self.assertTrue(learning.evaluate(time, "0.080 seconds")["correct"])

    def test_transfer_catalog_keys_and_public_view(self):
        problems = learning.catalog()["families"]["transfer"]
        self.assertEqual(len(problems), 3)
        self.assertEqual({p["questions"][0]["answer"] for p in problems}, {"1348 bytes", "1224 bytes", "1440 bytes"})
        for problem in problems:
            public = json.dumps(learning.public_problem(problem))
            self.assertNotIn('"answer"', public)
            self.assertNotIn('"explanation"', public)
            p = problem["parameters"]
            self.assertLessEqual(p["small_payload"] + p["ipv4_header"] + p["tcp_header"], p["mtu"])

    def test_all_families_cover_objectives_and_route_variants_change_the_reasoning(self):
        data = d.definition()
        problems = learning.catalog()["families"]
        self.assertTrue(data["learning_contract"]["enabled"])
        self.assertEqual(set(problems), set(data["learning_contract"]["families"]))
        for phase in data["phases"]:
            for binding in phase["assessment"].values():
                if binding["role"] == "conceptual":
                    for variant in problems[binding["family"]]:
                        self.assertIn(binding["field"], {q["id"] for q in variant["questions"]})
        expected = {
            "route-selection-r1": ("10.8.9.0/25", "10.8.9.0/25", {"10.0.0.2", "10.0.0.3"}, {"10.0.0.3"}),
            "route-selection-r2": ("192.0.2.128/26", "192.0.2.0/24", {"10.0.0.2"}, {"10.0.0.1"}),
        }
        for variant in problems["route-selection"][1:]:
            actual = {q["id"]: q["answer"] for q in variant["questions"]}
            before, after, hops, after_hops = expected[variant["id"]]
            self.assertEqual((actual["prefix"], actual["after-prefix"]), (before, after))
            self.assertEqual(set(actual["hops"].split(", ")), hops)
            self.assertEqual(set(actual["after-hops"].split(", ")), after_hops)
        for variant in problems["subnet"]:
            p = variant["parameters"]
            self.assertEqual(ipaddress.ip_interface(p["interface"]).network.prefixlen, 24)
            local = ipaddress.ip_address(p["peer"]) in ipaddress.ip_interface(p["interface"]).network
            self.assertEqual(variant["questions"][0]["answer"], "yes" if local else "no")
        for variant in problems["diagnosis"]:
            self.assertNotIn("case-a.json", json.dumps(variant))
            self.assertNotIn("case-b.json", json.dumps(variant))

    def test_every_authored_variant_against_independent_expected_facts(self):
        expected = {
            "transfer": [dict(payload="1348 bytes", fits="yes"), dict(payload="1224 bytes", fits="yes"), dict(payload="1440 bytes", fits="yes")],
            "subnet": [dict(local=v) for v in ("yes", "no", "yes")],
            "service-boundaries": [dict(dns=dns, application=app) for dns, app in (("no", "no"), ("yes", "no"), ("no", "yes"))],
            "route-selection": [dict(zip(("prefix", "after-prefix", "hops", "after-hops"), values)) for values in (
                ("10.1.2.3/32", "10.1.2.0/24", "10.0.0.4", "10.0.0.2, 10.0.0.3"),
                ("10.8.9.0/25", "10.8.9.0/25", "10.0.0.2, 10.0.0.3", "10.0.0.3"),
                ("192.0.2.128/26", "192.0.2.0/24", "10.0.0.2", "10.0.0.1"))],
            "convergence": [dict(interval=str(t), hop=h, application=a) for t,h,a in ((100,"10.255.1.2","no"),(65,"10.255.2.3","no"),(240,"10.255.3.4","yes"))],
            "bgp": [dict(peer=p) for p in ("192.0.2.2", "192.0.2.20", "192.0.2.40")],
            "routing-context": [dict(corp=c, isolated=i) for c,i in (("0.0.0.0/0","no route"),("198.51.100.0/24","no route"),("no route","203.0.113.0/28"))],
            "cloud": [dict(outbound=o, **{"return":r}) for o,r in (("on-prem","cloud"),("on-prem","no route"),("inspection","cloud"))],
            "policy": [dict(server=s, user=u) for s,u in (("allow","deny"),("deny","allow"),("allow","deny"))],
            "timestamps": [dict(utc=t) for t in ("2026-08-15T14:15:00Z", "2026-08-16T01:50:00Z", "2026-08-15T20:40:00Z")],
            "diagnosis": [dict(change=c, lookup=l, observation=o) for c,l,o in (
                ("10.30.0.0/16","no route","D3"),("QUARANTINE","no route","D2"),("10.40.0.0/16","0.0.0.0/0","D4"),
                ("MAINTENANCE","no route","D2"),("10.50.0.0/16","no route","D3"),("RESTRICTED","203.0.113.0/24","D4"),("10.60.0.0/16","0.0.0.0/0","D4"))],
        }
        problems = learning.catalog()["families"]
        self.assertEqual(set(expected), set(problems))
        for family, variants in problems.items():
            self.assertEqual(len(variants), len(expected[family]))
            for variant, answers in zip(variants, expected[family]):
                for question in variant["questions"]:
                    with self.subTest(variant=variant["id"], field=question["id"]):
                        self.assertTrue(learning.evaluate(question, answers[question["id"]])["correct"])
        for phase in d.definition()["phases"]:
            for family in {b["family"] for b in phase["assessment"].values() if b["role"] == "conceptual"}:
                state = dict(seed=1, learning=[])
                variant = learning.problem_action(state, phase, "reassess", {"family":family}, "synthetic-time")
                index = next(i for i,p in enumerate(problems[family]) if p["id"] == variant["id"])
                result = learning.problem_action(state, phase, "problem_answer", dict(variant_id=variant["id"], answers=expected[family][index]), "synthetic-time")
                self.assertTrue(result["independent"])
                for binding in phase["assessment"].values():
                    if binding["family"] == family:
                        self.assertTrue(learning.attained(state, binding["objective"]))
                self.assertFalse(learning.attained(state, "unrelated-objective"))


class TransferLearningJourneyTests(unittest.TestCase):
    request = journeys.SessionTests.request
    act = journeys.SessionTests.act
    reach_transfer = journeys.SessionTests.reach_transfer

    def setUp(self):
        journeys.SessionTests.setUp(self)
        self.reach_transfer()
        for _ in range(2):
            self.act("answer", {"text": "Prediction and evidence comparison"})
            self.act("continue")

    def test_wrong_feedback_help_resume_and_fresh_independent_success(self):
        original = {"text": "A size bound alone does not prove recovery.", "answers": {"transfer.payload": "1200 bytes"}}
        result = self.act("answer", original)
        self.assertEqual(result["result"]["checks"]["transfer.payload"]["feedback_code"], "missing-both-headers")
        self.act("reveal")
        self.act("answer", {**original, "answers": {"transfer.payload": "1160 bytes"}})
        self.assertFalse(self.view["result"]["checks"]["transfer.payload"]["independent"])
        self.act("support", {"family": "transfer", "level": "worked"})
        supported = self.view["result"]["problem_result"]["id"]
        self.act("problem_answer", {"variant_id": supported, "answers": {"payload": "1348 bytes", "fits": "yes"}})
        request = self.request("reassess", {"family": "transfer"})
        assigned = d.act("learner", request)
        self.assertEqual(d.act("learner", request), assigned)
        variant = assigned["result"]["problem_result"]
        resumed = d.session_status("learner")
        self.assertEqual(resumed["phase"]["problems"][-1]["problem"], variant)
        same = self.act("reassess", {"family": "transfer"})
        self.assertEqual(same["result"]["problem_result"], variant)
        payload = "1224 bytes" if variant["id"] == "transfer-r1" else "1440 bytes"
        self.act("problem_answer", {"variant_id": variant["id"], "answers": {"payload": payload, "fits": "yes"}})
        objective = next(o for o in self.view["objectives"] if o["family"] == "transfer")
        self.assertTrue(objective["fresh_independent"])
        self.assertFalse(objective["original_independent"])
        self.assertFalse(self.view["completion"]["objective_checks_satisfied"])
        exported = d.export_session("learner")
        self.assertNotIn('"answers"', json.dumps(exported))
        self.assertNotIn('"worked":', json.dumps(exported))

    def test_invalid_input_does_not_consume_and_exposed_variants_exhaust(self):
        before = d.session_status("learner")["revision"]
        with self.assertRaises(d.DeliveryError):
            self.act("answer", {"text": "Calculation", "answers": {"transfer.payload": "1160"}})
        self.assertEqual(d.session_status("learner")["revision"], before)
        for _ in range(2):
            variant = self.act("reassess", {"family": "transfer"})["result"]["problem_result"]
            self.act("problem_hint", {"variant_id": variant["id"]})
            payload = "1224 bytes" if variant["id"] == "transfer-r1" else "1440 bytes"
            result = self.act("problem_answer", {"variant_id": variant["id"], "answers": {"payload": payload, "fits": "yes"}})
            self.assertFalse(result["result"]["problem_result"]["independent"])
        self.assertTrue(self.act("reassess", {"family": "transfer"})["result"]["problem_result"]["exhausted"])

    def test_failed_fresh_answer_and_correction_do_not_become_independent(self):
        variant = self.act("reassess", {"family": "transfer"})["result"]["problem_result"]
        self.act("problem_answer", {"variant_id": variant["id"], "answers": {"payload": "1 bytes", "fits": "no"}})
        payload = "1224 bytes" if variant["id"] == "transfer-r1" else "1440 bytes"
        result = self.act("problem_answer", {"variant_id": variant["id"], "answers": {"payload": payload, "fits": "yes"}})
        self.assertFalse(result["result"]["problem_result"]["independent"])
        self.assertFalse(next(o for o in result["objectives"] if o["family"] == "transfer")["satisfied"])

    def test_predict_then_compute_bounds_and_preserve_baseline(self):
        baseline, hashes = d.experiment_baseline("transfer")
        with self.assertRaises(d.DeliveryError):
            self.act("experiment_result", {"experiment_id": "not-predicted"})
        result = self.act("experiment_predict", dict(parameters=dict(scenario="plain", payload=1160), prediction="This exactly fits; recovery remains unknown."))
        entry = result["result"]["experiment"]
        self.assertNotIn("result", entry)
        before = d.session_status("learner")["revision"]
        with self.assertRaises(d.DeliveryError):
            self.act("experiment_predict", dict(parameters=dict(scenario="plain", payload=1161), prediction="Too large"))
        self.assertEqual(d.session_status("learner")["revision"], before)
        result = self.act("experiment_result", {"experiment_id": entry["id"]})["result"]["experiment"]
        self.assertTrue(result["result"]["fits"])
        self.assertEqual(result["result"]["maximum_payload"], 1160)
        self.assertEqual(result["baseline_sha256"], hashes)
        self.assertEqual(d.experiment_baseline("transfer"), (baseline, hashes))
        self.assertTrue(d.session_status("learner")["phase"]["progress"]["exposed"])
        summary = d.export_session("learner")
        self.assertNotIn("This exactly fits", json.dumps(summary))

    def test_concurrent_assignment_and_corrupt_learning_history_preserve_work(self):
        request = self.request("reassess", {"family": "transfer"})
        def attempt(ident):
            try:
                return d.act("learner", {**request, "request_id": ident})["status"]
            except d.DeliveryError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(attempt, ("assignment-one", "assignment-two")))
        self.assertCountEqual(results, ["ok", 3])
        directory = d.session_dir("learner")
        state = d.load_state(directory, d.definition())
        self.assertEqual(len(state["learning"]), 1)
        state["learning"][0]["responses"] = [{"independent": True}]
        path = directory / "session.json"
        path.write_text(json.dumps(state))
        before = path.read_bytes()
        with self.assertRaisesRegex(d.DeliveryError, "Preserve this directory"):
            d.session_status("learner")
        self.assertEqual(path.read_bytes(), before)


class ExperimentTests(unittest.TestCase):
    def test_each_choice_changes_its_bounded_result(self):
        transfer, _ = d.experiment_baseline("transfer")
        result = lambda **params: learning.experiment("transfer", params, transfer)
        self.assertFalse(result(scenario="plain", payload=1161)["fits"])
        self.assertTrue(result(scenario="plain", payload=1160)["fits"])
        self.assertFalse(result(scenario="ip-options", payload=1160)["fits"])
        for parameters in ({"scenario": "shell", "payload": 128}, {"scenario": "plain", "payload": True}, {"scenario": "plain", "payload": 100000}, {"scenario": "plain", "payload": 128, "path": "/tmp/file"}):
            with self.assertRaises(ValueError):
                learning.experiment("transfer", parameters, transfer)
        routes, _ = d.experiment_baseline("routing")
        def route(condition, destination="10.0.20.40"):
            return learning.experiment("routing", dict(condition=condition, destination=destination), routes, d.workbench(1).select_routes, d.workbench(1).best_vrf_route)
        self.assertEqual(route("baseline")["prefix"], "10.0.20.40/32")
        self.assertEqual(route("remove-host-route")["next_hops"], ["10.0.10.253", "10.0.10.254"])
        self.assertEqual(route("OT", "198.51.100.77")["prefix"], "no route")
        failures, _ = d.experiment_baseline("resilience")
        params = dict(options=["state-sync", "monitoring"], failure="session-sync-stale", twist=False)
        first = learning.experiment("resilience", params, failures)
        second = learning.experiment("resilience", {**params, "options": ["backup-path", "management"]}, failures)
        self.assertNotEqual(first["addressed_dependencies"], second["addressed_dependencies"])
        twist = learning.experiment("resilience", {**params, "twist": True}, failures)
        self.assertGreater(len(twist["residual_risk"]), len(first["residual_risk"]))
        self.assertTrue(all(r["unknowns"] for r in (first, second, twist)))


class ArtifactLearningTests(unittest.TestCase):
    setUp = journeys.SessionTests.setUp
    request = journeys.SessionTests.request
    act = journeys.SessionTests.act
    experiment = journeys.SessionTests.experiment
    finish_day = journeys.SessionTests.finish_day
    review = journeys.SessionTests.review
    reach_transfer = journeys.SessionTests.reach_transfer

    def test_scoped_reviews_ignore_unrelated_regions_and_ledger_rows(self):
        self.finish_day()
        directory = d.session_dir("learner")
        journeys.fill_rehearsal_artifacts(directory)
        for phase in ("c01.review", "c05.review", "c06.review"):
            self.review(phase)
        packet = directory / "packet-path.md"
        original = packet.read_text()
        packet.write_bytes(original.replace("## Healthy Path — Challenge 1", "## My renamed heading").replace("\n", "\r\n").encode())
        self.assertTrue(d.session_status("learner")["reviews"]["c01.review"]["self"]["valid_pass"])
        incident = directory / "incident.md"
        incident.write_text(incident.read_text().replace("<!-- artifact:end exit -->", "Later exit revision.\n<!-- artifact:end exit -->"))
        self.assertTrue(d.session_status("learner")["reviews"]["c05.review"]["self"]["valid_pass"])
        self.assertTrue(d.session_status("learner")["reviews"]["c06.review"]["self"]["valid_pass"])
        ledger = directory / "evidence-ledger.csv"
        text = ledger.read_text()
        # The main-case row is unrelated to the original incident review.
        rows = text.splitlines(keepends=True)
        ledger.write_text("".join(row.replace("fixture entity", "revised entity") if row.startswith("A3,") else row for row in rows))
        status = d.session_status("learner")
        self.assertTrue(status["reviews"]["c05.review"]["self"]["valid_pass"])
        changed = status["reviews"]["c06.review"]["self"]["changed_dependencies"]
        self.assertEqual(changed, ["evidence-ledger.csv#A3"])
        saved = d.load_state(directory, d.definition())["phases"]["c06.review"]["reviews"][-1]
        self.assertIn("fixture entity", saved["dependency_snapshots"]["evidence-ledger.csv#A3"])
        ledger.write_text("".join(row for row in rows if not row.startswith("incident/auth.jsonl#2,")))
        self.assertFalse(d.session_status("learner")["reviews"]["c05.review"]["self"]["valid_pass"])

    def test_submit_region_records_snapshot_without_retyping_or_writing_file(self):
        self.reach_transfer()
        for _ in range(2):
            self.act("answer", {"text": "Observation and competing hypotheses"})
            self.act("continue")
        directory = d.session_dir("learner")
        journeys.fill_rehearsal_artifacts(directory)
        region = d.session_status("learner")["phase"]["artifact_regions"][0]
        path = directory / region["file"]
        before = path.read_bytes()
        payload = dict(file=region["file"], region=region["region"], expected_sha256=region["sha256"], answers={"transfer.payload": "1160 bytes"})
        self.act("submit_artifact", payload)
        self.assertEqual(path.read_bytes(), before)
        saved = self.view["phase"]["progress"]["submissions"][-1]
        self.assertEqual(saved["text"], region["text"])
        self.assertEqual(saved["artifact_source"]["sha256"], region["sha256"])
        path.write_text(path.read_text().replace("<!-- artifact:end c02 -->", "Revised claim.\n<!-- artifact:end c02 -->"))
        revision = d.session_status("learner")["revision"]
        with self.assertRaisesRegex(d.DeliveryError, "region changed"):
            self.act("submit_artifact", payload)
        self.assertEqual(d.session_status("learner")["revision"], revision)
        with self.assertRaises(d.DeliveryError):
            self.act("submit_artifact", {**payload, "file": "../elsewhere"})
        for bad in ("<!-- artifact:start c02 -->\ntext", "<!-- artifact:start c02 -->\n<!-- artifact:start c02 -->"):
            with self.assertRaisesRegex(d.DeliveryError, "artifact"):
                d.artifact_regions(bad)

    def test_calibration_is_formative_and_retains_scores_before_feedback(self):
        self.act("skip", {"reason": "Reach calibration"})
        self.act("skip", {"reason": "Reach calibration"})
        self.assertNotIn('"scores"', json.dumps(self.view["phase"]["calibration"]))
        for scores in (dict.fromkeys(d.DIMENSIONS, 1), dict(mechanism=2, evidence=2, uncertainty=0, action=1)):
            result = self.act("calibrate", dict(example_id="calibration-partial", scores=scores))
            self.assertTrue(result["result"]["calibration"]["formative"])
            self.assertEqual(result["result"]["calibration"]["scores"], scores)
        self.assertEqual(len(d.export_session("learner")["calibration"]), 2)
        self.assertFalse(self.view["completion"]["objective_checks_satisfied"])

    def test_terminal_submission_and_external_edit_conflict(self):
        self.reach_transfer()
        for _ in range(2):
            self.act("answer", {"text": "Initial hypothesis and observations"})
            self.act("continue")
        journeys.fill_rehearsal_artifacts(d.session_dir("learner"))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with mock.patch("sys.stdin.isatty", return_value=True), mock.patch("sys.stdout.isatty", return_value=True):
                with mock.patch("builtins.input", side_effect=("t", "1", "1160 bytes", "q")):
                    self.assertEqual(d.learn("learner"), 0)
        self.assertIn("Selected evidence:", output.getvalue())
        region = d.session_status("learner")["phase"]["artifact_regions"][0]
        path = d.session_dir("learner") / region["file"]
        original = learning.evaluate
        def edit_during_evaluation(item, response):
            if item["id"] == "transfer.payload":
                path.write_text(path.read_text().replace("<!-- artifact:end c02 -->", "External edit.\n<!-- artifact:end c02 -->"))
            return original(item, response)
        before = d.session_status("learner")["revision"]
        with mock.patch.object(learning, "evaluate", side_effect=edit_during_evaluation):
            with self.assertRaisesRegex(d.DeliveryError, "changed during submission"):
                self.act("submit_artifact", dict(file=region["file"], region=region["region"], expected_sha256=region["sha256"], answers={"transfer.payload": "1160 bytes"}))
        self.assertEqual(d.session_status("learner")["revision"], before)
        self.assertIn("External edit.", path.read_text())

    def test_invalid_reference_text_stays_private_and_unrelated_csv_record_is_ignored(self):
        self.finish_day()
        directory = d.session_dir("learner")
        journeys.fill_rehearsal_artifacts(directory)
        self.review("c05.review")
        ledger = directory / "evidence-ledger.csv"
        raw = ledger.read_text()
        row = next(row for row in csv.DictReader(io.StringIO(raw)) if row["evidence_id"] == "incident/flows.jsonl#1")
        record = d.workbench(3).read_jsonl("incident/flows.jsonl")[1]
        row.update(evidence_id="incident/flows.jsonl#2", raw_time=record["start"], normalized_time=record["start"])
        extra = io.StringIO(newline="")
        csv.DictWriter(extra, fieldnames=d.workbench(3).LEDGER_FIELDS).writerow(row)
        ledger.write_text(raw + extra.getvalue())
        self.assertEqual(d.ledger_errors(ledger.read_text(), d.load_state(directory, d.definition())), [])
        self.assertTrue(d.session_status("learner")["reviews"]["c05.review"]["self"]["valid_pass"])
        incident = directory / "incident.md"
        incident.write_text(incident.read_text().replace("Evidence IDs: incident/flows.jsonl#1", "Evidence IDs: PRIVATE PERSONAL NOTE", 1))
        self.assertNotIn("PRIVATE PERSONAL NOTE", json.dumps(d.export_session("learner")))
        with self.assertRaises(d.DeliveryError):
            d.ledger_records("evidence_id,source\ninvalid,header\n")

    def test_initial_diagnosis_gates_cues_and_old_state_is_preserved(self):
        while self.view["phase"]["id"] != "c06.receive":
            self.act("skip", {"reason": "Test setup"})
        phase = self.view["phase"]
        self.assertEqual(phase["assessment"], {})
        self.assertEqual(phase["artifact_regions"], [])
        self.assertEqual(phase["allowed_actions"], ["diagnose", "skip"])
        before = d.session_status("learner")["revision"]
        for action, payload in (("reveal", {}), ("answer", {"text": "Already diagnosed"}), ("evidence", {"view": "case.main"})):
            with self.assertRaises(d.DeliveryError):
                self.act(action, payload)
        self.assertEqual(d.session_status("learner")["revision"], before)
        self.act("diagnose", journeys.DIAGNOSIS)
        state_path = d.session_dir("learner") / "session.json"
        state = json.loads(state_path.read_text())
        state["schema_version"] = 1
        state_path.write_text(json.dumps(state))
        old = state_path.read_bytes()
        with self.assertRaisesRegex(d.DeliveryError, "matching course copy"):
            d.session_status("learner")
        self.assertEqual(state_path.read_bytes(), old)

    def test_targeted_support_preserves_unrelated_first_attempts(self):
        self.act("skip", {"reason": "Reach opening diagnostic"})
        self.act("support", {"family": "subnet", "level": "worked"})
        result = self.act("answer", dict(text="Different evidence is needed for each claim.",
                                          answers={"opening.local": "yes", "opening.dns": "no", "opening.application": "no"}))
        checks = result["result"]["checks"]
        self.assertFalse(checks["opening.local"]["independent"])
        self.assertTrue(checks["opening.dns"]["independent"])
        self.assertTrue(checks["opening.application"]["independent"])


if __name__ == "__main__":
    unittest.main()
