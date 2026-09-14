"""Offline checks for frozen coverage, durable attempts, and explicit resume."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import delivery as d
import llm
from test_llm import LOCAL


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        for patch in (mock.patch.object(d, "WORK_ROOT", Path(temporary.name)), mock.patch.dict(os.environ, LOCAL, clear=True)):
            patch.start()
            self.addCleanup(patch.stop)
        self.runner = d.module_at("verification/llm_run.py")
        self.cases = d.module_at("verification/llm_cases.py")

    def test_frozen_coverage_preflight_and_no_reserved_reassessment(self):
        coverage = self.cases.check()
        self.assertEqual(coverage["cases"], 112)
        self.assertEqual(coverage["families"], 11)
        self.assertEqual(len(coverage["excluded_objectives"]), 3)
        config = llm.configuration()
        from dataclasses import replace
        config = replace(config, response_format="json_schema", max_input_bytes=16384)
        for case in self.cases.cases():
            llm.prepare_request(config, case["feature"], case["context"])
        content = json.dumps(self.cases.cases())
        for problems in d.learning.catalog()["families"].values():
            for problem in problems:
                if problem["use"] == "reassessment":
                    self.assertNotIn(problem["id"], content)

    def test_durable_uncertain_attempt_is_never_resent_and_limits_persist(self):
        self.runner.create("durable")
        run = self.runner.Run("durable", "probe", llm.configuration(), "test")
        def interrupt(*args):
            self.assertEqual(run.load()["attempts"][-1]["status"], "pending")
            raise KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            run.call("first", "check", {}, generate=interrupt)
        with self.assertRaisesRegex(ValueError, "Uncertain prior attempt"):
            run.call("first", "check", {}, generate=lambda *args: self.fail("resent"))
        result = run.call("second", "check", {}, generate=lambda *args: dict(advice={"ready": True}))
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(run.call("second", "check", {}, generate=lambda *args: self.fail("resent")), result)
        with self.assertRaisesRegex(ValueError, "budget exhausted"):
            run.call("third", "check", {})
        with self.assertRaisesRegex(ValueError, "input changed"):
            run.call("second", "check", {"changed": True})
        with self.assertRaisesRegex(ValueError, "frozen configuration"):
            self.runner.Run("durable", "probe", llm.configuration(), "changed").call("second", "check", {})
        self.assertEqual(len(run.load()["attempts"]), 2)

    def test_explicit_resume_skips_recorded_results_and_preserves_inventory(self):
        self.runner.create("resume")
        generate = mock.Mock(return_value=dict(advice={"explanation": "Reason", "question": "How?", "evidence_ids": []}))
        with mock.patch.object(llm, "generate", generate):
            self.runner.batch("resume", "baseline", 2)
            with self.assertRaisesRegex(ValueError, "explicit --resume"):
                self.runner.batch("resume", "baseline", 2)
            self.runner.batch("resume", "baseline", 2, True)
        self.assertEqual(generate.call_count, 4)
        run = self.runner.Run("resume", "baseline", llm.configuration())
        state = run.load()
        state["cases"][0]["context"]["learner_text"] = "changed"
        d.save_state(run.directory, state)
        with self.assertRaisesRegex(ValueError, "inventory or limits changed"):
            run.load()


if __name__ == "__main__":
    unittest.main()
