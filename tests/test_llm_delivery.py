"""Advisory session behavior, release boundaries, and durable help exposure."""

import contextlib
import io
import json
import os
import unittest
from unittest import mock

import course
import delivery as d
import llm
import llm_delivery as support
import test_delivery as fixtures
from test_llm import LOCAL


class AdvisoryTests(unittest.TestCase):
    request = fixtures.SessionTests.request
    act = fixtures.SessionTests.act

    def setUp(self):
        settings = mock.patch.dict(os.environ, LOCAL, clear=True)
        settings.start()
        self.addCleanup(settings.stop)
        fixtures.SessionTests.setUp(self)

    def reach(self, phase):
        while self.view["phase"]["id"] != phase:
            self.act("skip", dict(reason="Synthetic LLM test setup"))

    def generated(self, config, feature, context):
        if feature == "review":
            advice = dict(findings=[dict(dimension="uncertainty", claim_quote="PRIVATE REHEARSAL TEXT",
                                        evidence_ids=["incident/auth.jsonl#2"],
                                        explanation="A login does not establish credential theft.",
                                        revision_question="What evidence would distinguish authorized use?")], insufficient_evidence=False)
        elif feature == "coach":
            advice = dict(explanation="Consider both headers in the stated bound.",
                          question="Which header did your calculation include?", evidence_ids=[])
        else:
            advice = dict(question="Who owns the next check and how will it be validated?", evidence_ids=[])
        return dict(advice=advice, model=config.model, endpoint=config.base_url,
                    prompt_version=llm.PROMPT_VERSION, usage={}, latency_ms=1)

    def open_view(self, phase, view):
        command = d.evidence_command(view, dict(case="A"))
        source = next(arg for arg in command if arg.startswith("labs/fixtures/"))
        value = (d.ROOT / source).read_text()
        if view.startswith("case.main."):
            packet = json.loads(value)
            keys = {"state": ("before", "after", "routes", "flow"), "observations": ("observations",),
                    "conditions": ("conditions", "limitations", "path", "scope")}[view.rsplit(".", 1)[1]]
            value = json.dumps({key: packet[key] for key in keys})
        with mock.patch.object(d, "run_tool", return_value=dict(returncode=0, truncated=False, stdout=value)):
            self.act("evidence", dict(view=view), phase)

    def prepare_review(self):
        self.reach("c05.narrative")
        fixtures.fill_rehearsal_artifacts(d.session_dir("learner"))
        for number in (1, 2, 3):
            self.open_view(f"c05.round{number}", f"incident.round{number}")
        self.act("answer", dict(text="PRIVATE submitted narrative"))
        self.act("continue")

    def prepare_coach(self, correct=False):
        self.reach("c02.calculate")
        self.act("answer", dict(text="PRIVATE calculation", answers={"transfer.payload": "1160 bytes" if correct else "1200 bytes"}))

    def test_review_context_citations_snapshots_and_private_export(self):
        self.prepare_review()
        before = d.export_session("learner")["completion"]
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            request = self.request("llm_review")
            result = d.act("learner", request)
            context = generate.call_args.args[2]
            self.assertIn("incident/auth.jsonl#2", context["evidence"])
            self.assertNotIn("c06-handoff", context["regions"])
            self.assertNotIn("B-v1", json.dumps(context))
            self.assertNotIn("transfer-r1", json.dumps(context))
            self.assertEqual(result["result"]["learning_result"], "advisory_complete")
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(d.act("learner", request), result)
            self.assertEqual(generate.call_count, 1)
        self.assertEqual(d.export_session("learner")["completion"], before)
        public = json.dumps(d.export_session("learner"))
        self.assertNotIn("PRIVATE", public)
        self.assertNotIn("distinguish authorized", public)
        private = d.export_session("learner", True)
        self.assertIn("distinguish authorized", json.dumps(private))
        self.assertIn("distinguish authorized", d.format_export(private, "markdown"))
        self.assertFalse(d.load_state(d.session_dir("learner"), d.definition())["phases"]["c05.review"]["reviews"])

    def test_help_exposes_assigned_variant_but_preserves_independent_original(self):
        self.prepare_coach(correct=True)
        self.act("reassess", dict(family="transfer"))
        with mock.patch.object(llm, "generate", side_effect=self.generated):
            result = self.act("llm_coach", dict(family="transfer"))
        self.assertTrue(result["phase"]["progress"]["checks"]["transfer.payload"]["independent"])
        state = d.load_state(d.session_dir("learner"), d.definition())
        self.assertTrue(state["learning"][0]["exposed"])
        self.assertNotIn("m1.routes.10.0.20.40", state["phases"]["c01.change"]["exposed_checks"])

    def test_pending_duplicate_interruption_and_cancel_with_feature_disabled(self):
        self.prepare_coach()
        request = self.request("llm_coach", dict(family="transfer"))
        with mock.patch.object(llm, "generate", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                d.act("learner", request)
        with mock.patch.object(llm, "generate", side_effect=AssertionError("duplicate inference")):
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_pending")
            with self.assertRaises(d.DeliveryError):
                self.act("llm_coach", dict(family="transfer"))
            with self.assertRaises(d.DeliveryError):
                d.act("learner", {**request, "action": "skip", "payload": {"reason": "ID collision"}})
            with mock.patch.dict(os.environ, {}, clear=True):
                self.act("llm_cancel", dict(request_id=request["request_id"]))
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_cancelled")
        self.assertFalse(d.session_status("learner")["phase"]["progress"]["exposed"])

    def test_inference_releases_lock_and_discards_concurrent_changes(self):
        self.prepare_coach()
        request = self.request("llm_coach", dict(family="transfer"))

        def change(config, feature, context):
            self.assertEqual(d.act("learner", request)["result"]["learning_result"], "advisory_pending")
            self.act("answer", dict(text="A concurrent correction", answers={"transfer.payload": "1160 bytes"}))
            return self.generated(config, feature, context)

        with mock.patch.object(llm, "generate", side_effect=change):
            result = d.act("learner", request)
        self.assertEqual(result["result"]["learning_result"], "advisory_stale")
        self.assertNotIn("advice", result["result"])
        self.assertFalse(result["phase"]["progress"]["exposed"])

    def test_artifact_edits_make_pending_advice_stale(self):
        self.prepare_review()

        def change(config, feature, context):
            path = d.session_dir("learner") / "incident.md"
            path.write_text(path.read_text().replace("PRIVATE REHEARSAL TEXT", "Edited narrative"))
            return self.generated(config, feature, context)

        with mock.patch.object(llm, "generate", side_effect=change):
            result = self.act("llm_review")
        self.assertEqual(result["result"]["learning_result"], "advisory_stale")
        self.assertFalse(result["phase"]["progress"]["exposed"])

    def test_failure_preserves_assessment_and_can_resume_without_config(self):
        self.prepare_coach()
        with mock.patch.object(llm, "generate", side_effect=llm.LLMError("Unavailable", "unavailable")):
            result = self.act("llm_coach", dict(family="transfer"))
        self.assertEqual(result["result"]["learning_result"], "advisory_failed")
        self.assertFalse(result["phase"]["progress"]["exposed"])
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": "broken"}):
            self.assertEqual(d.session_status("learner")["llm"]["configuration"]["status"], "configuration")
            self.act("answer", dict(text="Correction", answers={"transfer.payload": "1160 bytes"}))

    def test_first_response_required_and_exit_always_excluded(self):
        self.reach("c02.calculate")
        before = (d.session_dir("learner") / "session.json").read_bytes()
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            with self.assertRaises(d.DeliveryError):
                self.act("llm_coach", dict(family="transfer"))
            self.assertEqual((d.session_dir("learner") / "session.json").read_bytes(), before)
            with self.assertRaises(d.DeliveryError):
                self.act("llm_review", phase="exit.review")
        self.reach("exit.answer")
        self.assertFalse(any(a.startswith("llm_") for a in d.session_status("learner")["phase"]["allowed_actions"]))

    def test_unopened_citations_do_not_fetch_more_evidence(self):
        self.prepare_review()
        state = d.load_state(d.session_dir("learner"), d.definition())
        state["phases"]["c05.round2"]["views"] = []
        d.save_state(d.session_dir("learner"), state)
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            with self.assertRaisesRegex(d.DeliveryError, "Open the evidence views"):
                self.act("llm_review")
        phase = d.phase_by_id(d.definition(), "c05.round2")
        evidence = support.opened_evidence(state, d.definition(), phase)
        self.assertNotIn("view:incident.round3", evidence)
        self.assertNotIn("incident/auth.jsonl#2", evidence)

    def test_handoff_uses_only_opened_case_fields_and_limits_three_turns(self):
        self.reach("c06.receive")
        self.act("diagnose", fixtures.DIAGNOSIS)
        self.reach("c06.analyze")
        self.open_view("c06.analyze", "case.main.observations")
        self.act("answer", dict(text="PRIVATE analysis", answers=fixtures.answers_for(self.view["phase"], "A")))
        self.act("continue")
        fixtures.fill_rehearsal_artifacts(d.session_dir("learner"))
        self.act("answer", dict(text="PRIVATE handoff"))
        self.act("continue")
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            for index in range(3):
                self.act("llm_handoff", dict(role="network-operations", text="A recipient reply" if index else ""))
            context = generate.call_args.args[2]
            self.assertNotIn("view:case.main.state", context["evidence"])
            self.assertNotIn("view:case.main.conditions", context["evidence"])
            self.assertEqual(len(context["exchange"]), 2)
            with self.assertRaisesRegex(d.DeliveryError, "three model turns"):
                self.act("llm_handoff", dict(role="security", text="One more"))
            path = d.session_dir("learner") / "incident.md"
            path.write_text(path.read_text().replace("PRIVATE REHEARSAL TEXT", "Revised PRIVATE REHEARSAL TEXT"))
            self.act("llm_handoff", dict(role="security", text=""))
            self.assertEqual(generate.call_count, 4)

    def test_terminal_and_cli_share_the_session_action(self):
        self.prepare_coach()
        output = io.StringIO()
        with mock.patch.object(llm, "generate", side_effect=self.generated), contextlib.redirect_stdout(output):
            self.assertEqual(course.main(["llm", "coach", "--id", "learner", "--phase", "c02.calculate", "--family", "transfer", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["result"]["learning_result"], "advisory_complete")
        with contextlib.redirect_stdout(io.StringIO()) as output, mock.patch.object(d.sys.stdin, "isatty", return_value=True), \
                mock.patch.object(d.sys.stdout, "isatty", return_value=True), \
                mock.patch("builtins.input", side_effect=["lc", "transfer", "q"]), \
                mock.patch.object(llm, "generate", side_effect=self.generated):
            self.assertEqual(d.learn("learner"), 0)
        self.assertIn("Which header", output.getvalue())
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(course.main(["llm", "coach", "--json"]), 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "error")


if __name__ == "__main__":
    unittest.main()
