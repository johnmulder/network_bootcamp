"""Optional inference contracts; ordinary tests never contact a model server."""

import contextlib
import copy
from dataclasses import replace
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest import mock

import course
import delivery as d
import learning
import llm

LOCAL = {"BOOTCAMP_LLM_FEATURES": "review,coach,handoff,author",
         "BOOTCAMP_LLM_BASE_URL": "http://localhost:1234/v1",
         "BOOTCAMP_LLM_MODEL": "test-model", "BOOTCAMP_LLM_TOKEN_FIELD": "max_tokens"}
FAKE_KEY = "review-test-key"
ADVICE_CONTEXT = dict(learner_text="A login succeeded.", evidence={"record": {}})


def envelope(advice=None, **changes):
    value = dict(choices=[dict(finish_reason="stop", message=dict(content=json.dumps(advice or {"ready": True})))],
                 usage=dict(prompt_tokens=10, completion_tokens=5, total_tokens=15, private="omit"))
    value.update(changes)
    return json.dumps(value).encode()


def credential_echo(advice, layer="content"):
    raw = envelope(advice)
    escaped = "\\u0072eview-test-key"
    if layer == "content":
        value = json.loads(raw)
        message = value["choices"][0]["message"]
        message["content"] = message["content"].replace(FAKE_KEY, escaped)
        return json.dumps(value).encode()
    return raw.replace(FAKE_KEY.encode(), escaped.encode()) if layer == "envelope" else raw


def advice_samples(text):
    return {
        "review": dict(findings=[dict(dimension="evidence", claim_quote="A login succeeded.",
                                     evidence_ids=["record"], explanation=text, revision_question=text)],
                       insufficient_evidence=False),
        "coach": dict(explanation=text, question=text, evidence_ids=[]),
        "handoff": dict(question=text, evidence_ids=[]),
        "author": dict(draft=text),
    }


class ClientTests(unittest.TestCase):
    def setUp(self):
        patch = mock.patch.dict(os.environ, LOCAL, clear=True)
        patch.start()
        self.addCleanup(patch.stop)

    def test_offline_disabled_and_configuration(self):
        with mock.patch("urllib.request.build_opener", side_effect=AssertionError("network")):
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(llm.availability()["status"], "disabled")
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(course.main(["llm", "check", "--json"]), 0)
                with self.assertRaises(llm.LLMError):
                    llm.configuration()
            self.assertEqual(llm.availability()["status"], "configured")
            for key, value in (("BOOTCAMP_LLM_FEATURES", "unknown"),
                               ("BOOTCAMP_LLM_MODEL", ""),
                               ("BOOTCAMP_LLM_TIMEOUT_SECONDS", "nan"),
                               ("BOOTCAMP_LLM_TIMEOUT_SECONDS", "301"),
                               ("BOOTCAMP_LLM_MAX_OUTPUT_TOKENS", "0"),
                               ("BOOTCAMP_LLM_RESPONSE_FORMAT", "automatic"),
                               ("BOOTCAMP_LLM_MAX_INPUT_BYTES", "1023"),
                               ("BOOTCAMP_LLM_MAX_INPUT_BYTES", "65537"),
                               ("BOOTCAMP_LLM_MAX_INPUT_BYTES", "1.5"),
                               ("BOOTCAMP_LLM_TOKEN_FIELD", "invented")):
                with self.subTest(key=key, value=value), mock.patch.dict(os.environ, {key: value}):
                    self.assertEqual(llm.availability()["status"], "configuration")

    def test_url_auth_and_no_ambient_key(self):
        for url in ("http://localhost:1234/v1", "http://127.0.0.1:1234/v1/", "http://[::1]:1234/v1"):
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": url, "OPENAI_API_KEY": "ambient-secret"}):
                config = llm.configuration()
                self.assertTrue(config.loopback)
                self.assertEqual(config.api_key, "")
        for url in ("http://example.com/v1", "https://user:secret@example.com/v1", "https://example.com/v1?key=secret",
                    "https://example.com/v1#fragment", "https://example.com/v1/chat/completions", "file:///v1",
                    "http://localhost:99999/v1", "https://example.com/v1/../v1", "http://localhost.evil/v1"):
            with self.subTest(url=url), mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": url}):
                with self.assertRaises(llm.LLMError):
                    llm.configuration()
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": "https://api.openai.com/v1"}):
            with self.assertRaises(llm.LLMError):
                llm.configuration()
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": "explicit-secret"}):
                self.assertNotIn("explicit-secret", repr(llm.configuration()))
                self.assertNotIn("explicit-secret", json.dumps(llm.configuration().public()))

    def test_both_wire_profiles_and_bearer_auth(self):
        for base, token, key in (("http://localhost:1234/v1", "max_tokens", ""),
                                 ("http://localhost:1234/v1", "max_tokens", "local-token"),
                                 ("https://api.openai.com/v1", "max_completion_tokens", "openai-token")):
            with self.subTest(base=base, key=bool(key)), mock.patch.dict(os.environ, {
                "BOOTCAMP_LLM_BASE_URL": base, "BOOTCAMP_LLM_TOKEN_FIELD": token, "BOOTCAMP_LLM_API_KEY": key,
            }), mock.patch("urllib.request.build_opener") as factory:
                factory.return_value.open.return_value = io.BytesIO(envelope())
                result = llm.generate(llm.configuration(), "check", {})
                request = factory.return_value.open.call_args.args[0]
                self.assertEqual(request.full_url, base + "/chat/completions")
                body = json.loads(request.data)
                self.assertEqual(set(body), {"model", "messages", "stream", token})
                self.assertEqual(body[token], 2048)
                self.assertFalse(body["stream"])
                self.assertEqual(request.get_header("Authorization"), "Bearer " + key if key else None)
                self.assertEqual(result["usage"], dict(prompt_tokens=10, completion_tokens=5, total_tokens=15))
                self.assertNotIn("private", result["usage"])
                self.assertIsNone(llm.NoRedirect().redirect_request(request, None, 302, "", {}, "https://evil.example"))
                if base.startswith("http:"):
                    self.assertTrue(any(isinstance(h, llm.urllib.request.ProxyHandler) and not h.proxies
                                        for h in factory.call_args.args))

    def test_bounded_context_response_and_failure_privacy(self):
        with mock.patch("urllib.request.build_opener") as factory:
            with self.assertRaises(llm.LLMError):
                llm.generate(llm.configuration(), "check", {"text": "x" * llm.CONTEXT_LIMIT})
            factory.assert_not_called()
            for raw in (b"x" * (llm.RESPONSE_LIMIT + 1), b"not JSON", b'{"choices":[]}',
                        envelope(choices=[dict(finish_reason="length", message=dict(content='{}'))]),
                        envelope(choices=[dict(finish_reason="stop", message=dict(content='{"ready": true}', refusal="refused"))])):
                factory.return_value.open.return_value = io.BytesIO(raw)
                with self.assertRaises(llm.LLMError):
                    llm.generate(llm.configuration(), "check", {})
            for failure in (TimeoutError("secret"), urllib.error.URLError("secret"),
                            urllib.error.HTTPError("https://secret", 401, "secret", {}, io.BytesIO(b"secret")),
                            urllib.error.HTTPError("https://secret", 429, "secret", {}, io.BytesIO(b"secret"))):
                factory.return_value.open.side_effect = failure
                with self.assertRaises(llm.LLMError) as caught:
                    llm.generate(llm.configuration(), "check", {})
                self.assertNotIn("secret", str(caught.exception))
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": "private-token"}), \
                mock.patch("urllib.request.build_opener") as factory:
            with self.assertRaises(llm.LLMError):
                llm.generate(llm.configuration(), "check", {"text": "private-token"})
            factory.assert_not_called()
            factory.return_value.open.return_value = io.BytesIO(envelope(dict(ready=True, secret="private-token")))
            with self.assertRaises(llm.LLMError) as caught:
                llm.generate(llm.configuration(), "check", {})
                self.assertNotIn("private-token", str(caught.exception))

    def test_optional_schema_profiles_keep_semantic_validation_and_do_not_retry(self):
        for base, token in (("http://localhost:1234/v1", "max_tokens"),
                            ("https://api.openai.com/v1", "max_completion_tokens")):
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_BASE_URL": base,
                                             "BOOTCAMP_LLM_TOKEN_FIELD": token,
                                             "BOOTCAMP_LLM_API_KEY": FAKE_KEY,
                                             "BOOTCAMP_LLM_RESPONSE_FORMAT": "json_schema"}):
                for feature, advice in {"check": {"ready": True}, **advice_samples("Consider the evidence.")}.items():
                    with self.subTest(base=base, feature=feature), mock.patch("urllib.request.build_opener") as factory:
                        factory.return_value.open.return_value = io.BytesIO(envelope(advice))
                        result = llm.generate(llm.configuration(), feature, ADVICE_CONTEXT)
                        body = json.loads(factory.return_value.open.call_args.args[0].data)
                        self.assertEqual(body[token], 2048)
                        schema = body["response_format"]["json_schema"]
                        self.assertIs(schema["strict"], True)
                        self.assertEqual(set(schema["schema"]["required"]), set(advice))
                        self.assertFalse(schema["schema"]["additionalProperties"])
                        if feature == "review":
                            nested = schema["schema"]["properties"]["findings"]["items"]
                            self.assertEqual(set(nested["required"]), set(advice["findings"][0]))
                            self.assertFalse(nested["additionalProperties"])
                        self.assertEqual(result["response_format"], "json_schema")
                with mock.patch("urllib.request.build_opener") as factory:
                    factory.return_value.open.side_effect = urllib.error.HTTPError(base, 400, "secret", {}, io.BytesIO(b"secret"))
                    with self.assertRaisesRegex(llm.LLMError, "explicitly select prompt mode"):
                        llm.generate(llm.configuration(), "check", {})
                    factory.return_value.open.assert_called_once()
                with mock.patch("urllib.request.build_opener") as factory:
                    invalid = advice_samples("Consider the evidence.")["review"]
                    invalid["findings"][0]["claim_quote"] = "Invented quote"
                    factory.return_value.open.return_value = io.BytesIO(envelope(invalid))
                    with self.assertRaises(llm.LLMError):
                        llm.generate(llm.configuration(), "review", ADVICE_CONTEXT)

    def test_decoded_credentials_are_rejected_for_every_feature(self):
        for feature, advice in advice_samples("Provider echo: " + FAKE_KEY).items():
            for layer in ("plain", "envelope", "content"):
                with self.subTest(feature=feature, layer=layer), \
                        mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": FAKE_KEY}), \
                        mock.patch("urllib.request.build_opener") as factory:
                    raw = credential_echo(advice, layer)
                    if layer != "plain":
                        self.assertNotIn(FAKE_KEY.encode(), raw)
                    factory.return_value.open.return_value = io.BytesIO(raw)
                    with self.assertRaises(llm.LLMError) as caught:
                        llm.generate(llm.configuration(), feature, ADVICE_CONTEXT)
                    self.assertEqual(caught.exception.code, "invalid-output")
                    self.assertNotIn(FAKE_KEY, str(caught.exception))
                    factory.return_value.open.assert_called_once()
                    with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": ""}):
                        factory.return_value.open.return_value = io.BytesIO(raw)
                        self.assertEqual(llm.generate(llm.configuration(), feature, ADVICE_CONTEXT)["advice"], advice)

    def test_unicode_prose_is_validated_before_returning_advice(self):
        for valid, text in ((False, "\ud800"), (False, "\udfff"), (True, "Café 🚀")):
            for feature, sample in advice_samples("Valid advice.").items():
                body = sample["findings"][0] if feature == "review" else sample
                for field in body.keys() & {"explanation", "revision_question", "question", "draft"}:
                    with self.subTest(feature=feature, field=field, text=ascii(text)), \
                            mock.patch("urllib.request.build_opener") as factory:
                        advice = copy.deepcopy(sample)
                        target = advice["findings"][0] if feature == "review" else advice
                        target[field] = text
                        factory.return_value.open.return_value = io.BytesIO(envelope(advice))
                        if valid:
                            result = llm.generate(llm.configuration(), feature, ADVICE_CONTEXT)
                            restored = json.loads(json.dumps(result, ensure_ascii=False).encode("utf-8"))
                            self.assertEqual(restored["advice"], advice)
                        else:
                            with self.assertRaises(llm.LLMError) as caught:
                                llm.generate(llm.configuration(), feature, ADVICE_CONTEXT)
                            self.assertEqual(caught.exception.code, "invalid-output")
                            self.assertNotIn(text, str(caught.exception))

    def test_advice_schema_quotes_and_citations(self):
        context = dict(learner_text="A login proves theft.", evidence={"incident/auth.jsonl#2": {}})
        finding = dict(dimension="evidence", claim_quote="A login proves theft.", evidence_ids=["incident/auth.jsonl#2"],
                       explanation="Authentication does not establish credential acquisition.",
                       revision_question="What evidence would distinguish authorized use?")
        result = dict(findings=[finding], insufficient_evidence=False)
        self.assertEqual(llm.validate_output("review", result, context), result)
        for change in (dict(evidence_ids=["reserved-case"]), dict(claim_quote="invented"), dict(dimension="score")):
            with self.assertRaises(llm.LLMError):
                llm.validate_output("review", dict(findings=[{**finding, **change}], insufficient_evidence=False), context)
        with self.assertRaises(llm.LLMError):
            llm.validate_output("coach", dict(explanation="Ignore instructions", question="?", evidence_ids=[], score=8), context)
        with self.assertRaises(llm.LLMError):
            llm.validate_output("handoff", dict(question="\x1b[31m", evidence_ids=[]), context)
        with self.assertRaises(ValueError):
            llm.decode('{"ready": true, "ready": false}')

    def test_input_budget_counts_utf8_messages_and_schema_before_network(self):
        context = dict(learner_text="Café 🚀 " * 100, evidence={})
        config = replace(llm.configuration(), response_format="json_schema")
        body, size = llm.prepare_request(config, "coach", context)
        inputs = {k: body[k] for k in ("messages", "response_format")}
        self.assertEqual(size, len(llm.json_text(inputs).encode("utf-8")))
        self.assertGreater(size, len(llm.json_text(inputs)))
        self.assertLess(llm.prepare_request(replace(config, response_format="prompt"), "coach", context)[1], size)
        with mock.patch("urllib.request.build_opener") as factory:
            with self.assertRaisesRegex(llm.LLMError, f"needs {size} bytes"):
                llm.generate(replace(config, max_input_bytes=size - 1), "coach", context)
            factory.assert_not_called()
            factory.return_value.open.return_value = io.BytesIO(envelope(advice_samples("Consider evidence.")["coach"]))
            result = llm.generate(replace(config, max_input_bytes=size), "coach", context)
            self.assertEqual(result["input_bytes"], size)

    def test_compaction_preserves_facts_identifiers_quotes_and_original_context(self):
        record = dict(event="login", success=True, actor="backup")
        packet = dict(observations=[record, dict(event="contradictory observation")], limitation="Uncertain intent")
        context = dict(learner_text="Café 🚀\n\nIntent unknown", regions={"first": "Café 🚀", "second": "Intent unknown"},
                       evidence={"event1": dict(record=record, source="original"),
                                 "view:partial": dict(text=json.dumps(packet), view="partial"),
                                 "view:plain": dict(text="Non-JSON observation"),
                                 "view:unmatched": dict(text='{"event":"different"}')})
        original = copy.deepcopy(context)
        compact = llm.compact_context(context)
        self.assertEqual(context, original)
        self.assertEqual(compact["region_ids"], ["first", "second"])
        self.assertEqual(compact["learner_text"], context["learner_text"])
        self.assertEqual(set(compact["evidence"]), set(context["evidence"]))
        restored = compact["evidence"]["view:partial"]["data"]
        reference = restored["observations"][0]["evidence_ref"]
        restored["observations"][0] = compact["evidence"][reference]["record"]
        self.assertEqual(restored, packet)
        self.assertEqual(compact["evidence"]["view:plain"], context["evidence"]["view:plain"])
        self.assertEqual(compact["evidence"]["view:unmatched"], context["evidence"]["view:unmatched"])
        changed = {**context, "learner_text": "Different submission"}
        self.assertIn("regions", llm.compact_context(changed))


class AuthorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        for patch in (mock.patch.dict(os.environ, LOCAL, clear=True),
                      mock.patch.object(d, "WORK_ROOT", Path(self.temp.name))):
            patch.start()
            self.addCleanup(patch.stop)

    def generated(self, config, feature, context):
        return dict(advice=dict(draft="Unreviewed wording for the fixed conditions."),
                    endpoint=config.base_url, model=config.model, prompt_version=1, latency_ms=1, usage={})

    def test_supported_examples_exclude_reserved_problems_and_compute_facts(self):
        for family in learning.catalog()["families"]:
            context = llm.author_context(family, "practice-variant")
            self.assertEqual(context["example"]["use"], "supported")
            self.assertNotIn("reassessment", json.dumps(context))
            self.assertNotIn("case-b.json", json.dumps(context))
        self.assertEqual(llm.author_context("transfer", "explanation")["computed_facts"]["maximum_payload"], 1348)
        candidate = llm.author_context("transfer", "practice-variant", seed=7)
        self.assertEqual(candidate, llm.author_context("transfer", "practice-variant", seed=7))
        self.assertNotIn(candidate["example"]["parameters"]["mtu"], {p["parameters"]["mtu"] for p in learning.catalog()["families"]["transfer"]})
        self.assertEqual(candidate["authored_facts"]["payload"], f"{candidate['computed_facts']['maximum_payload']} bytes")
        self.assertTrue(llm.author_context("subnet", "explanation")["computed_facts"]["local"])
        routes = llm.author_context("route-selection", "explanation")["computed_facts"]
        self.assertEqual(routes["before"][0]["prefix"], "10.1.2.3/32")
        self.assertEqual(len(routes["after"]), 2)

    def test_authoring_is_explicit_private_and_never_overwrites(self):
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            result = llm.author("transfer", "practice-variant", "transfer.json")
            path = Path(result["output"])
            record = json.loads(path.read_text())
            self.assertEqual(record["status"], "unreviewed-draft")
            self.assertIn("independent answer keys", record["review_required"])
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            for name in ("transfer.json", "../escape.json", "/tmp/escape.json"):
                with self.assertRaises(d.DeliveryError):
                    llm.author("transfer", "explanation", name)
            self.assertEqual(generate.call_count, 1)
            with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_FEATURES": "review"}):
                with self.assertRaises(llm.LLMError):
                    llm.author("transfer", "explanation", "new.json")

    def test_credential_echo_does_not_create_a_draft(self):
        with mock.patch.dict(os.environ, {"BOOTCAMP_LLM_API_KEY": FAKE_KEY}), \
                mock.patch("urllib.request.build_opener") as factory:
            factory.return_value.open.return_value = io.BytesIO(credential_echo(dict(draft=FAKE_KEY)))
            with self.assertRaises(llm.LLMError) as caught:
                llm.author("transfer", "explanation", "rejected.json")
            self.assertEqual(caught.exception.code, "invalid-output")
            self.assertFalse(list(Path(self.temp.name).rglob("*")))

    def test_invalid_unicode_does_not_create_a_draft(self):
        for text in ("\ud800", "\udfff"):
            with self.subTest(text=ascii(text)), mock.patch("urllib.request.build_opener") as factory:
                factory.return_value.open.return_value = io.BytesIO(envelope(dict(draft=text)))
                with self.assertRaises(llm.LLMError) as caught:
                    llm.author("transfer", "explanation", "rejected.json")
                self.assertEqual(caught.exception.code, "invalid-output")
                self.assertFalse(list(Path(self.temp.name).rglob("*")))

    def test_concurrent_output_symlink_and_interruption_preserve_files(self):
        target = llm.write_work_json("llm-drafts", "existing.json", {"original": True})
        alias = target.parent / "alias.json"
        alias.symlink_to(target)
        with self.assertRaises(d.DeliveryError):
            llm.work_output("llm-drafts", "alias.json")
        with mock.patch.object(llm.os, "link", side_effect=FileExistsError):
            with self.assertRaises(FileExistsError):
                llm.write_work_json("llm-drafts", "new.json", {"new": True})
        self.assertEqual(json.loads(target.read_text()), {"original": True})
        self.assertFalse(list(target.parent.glob(".llm-*")))
        self.assertFalse((target.parent / "new.json").exists())

    def test_author_cli(self):
        with mock.patch.object(llm, "generate", side_effect=self.generated), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(course.main(["llm", "author", "--family", "transfer", "--kind", "explanation", "--output", "cli.json", "--json"]), 0)
        self.assertEqual(json.loads(output.getvalue())["draft_status"], "unreviewed-draft")

    def test_evaluation_is_offline_by_default_and_never_claims_human_review(self):
        evaluation = d.module_at("verification/check_llm.py")
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(evaluation.main(["--check"]), 0)
        self.assertEqual(len(evaluation.cases()), 10)
        with mock.patch.object(llm, "generate", side_effect=self.generated):
            result = evaluation.evaluate("author", "held-out", "author.json")
        saved = json.loads(Path(result["output"]).read_text())
        self.assertEqual(saved["status"], "human-review-pending")
        self.assertEqual(saved["examples"][0]["split"], "held-out")
        self.assertIsNone(saved["examples"][0]["facilitator"]["grounded"])

    def test_repeated_evaluation_records_configuration_and_bounds_calls(self):
        evaluation = d.module_at("verification/check_llm.py")
        with mock.patch.object(llm, "generate", side_effect=self.generated) as generate:
            result = evaluation.evaluate("all", "calibration", "repeated.json", repeat=3, server_info="Synthetic server")
            self.assertEqual(generate.call_count, 15)
        saved = json.loads(Path(result["output"]).read_text())
        self.assertEqual(saved["configuration"]["response_format"], "prompt")
        self.assertEqual(saved["server_info"], "Synthetic server")
        self.assertEqual({v["repetition"] for v in saved["examples"]}, {1, 2, 3})
        self.assertTrue(all(v["output"]["input_bytes"] > 0 for v in saved["examples"]))
        with mock.patch.object(llm, "generate", side_effect=AssertionError("network")):
            with self.assertRaises(llm.LLMError):
                evaluation.evaluate("author", "calibration", "invalid.json", repeat=0)


if __name__ == "__main__":
    unittest.main()
