"""Learning contracts and independent checks of authored problems."""

import json
import ipaddress
import unittest
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
            local = ipaddress.ip_address(p["peer"]) in ipaddress.ip_interface(p["interface"]).network
            self.assertEqual(variant["questions"][0]["answer"], "yes" if local else "no")
        for variant in problems["diagnosis"]:
            self.assertNotIn("case-a.json", json.dumps(variant))
            self.assertNotIn("case-b.json", json.dumps(variant))


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
        self.assertNotIn('"worked"', json.dumps(exported))

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


if __name__ == "__main__":
    unittest.main()
