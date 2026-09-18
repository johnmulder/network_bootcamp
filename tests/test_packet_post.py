"""Practice correctness and recovery, without tcod or a display."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from packet_post import content
from packet_post.game import Game, Save
from packet_post.view import UI, feedback_text


class PacketPostTests(unittest.TestCase):
    def test_keyboard_controller_keeps_text_and_focus_then_resumes(self):
        with tempfile.TemporaryDirectory() as temp:
            with Save("keyboard", Path(temp)) as save:
                game = Game()
                ui = UI(game, save)
                ui.key("ENTER")
                ui.key("ENTER")
                for _ in range(3):
                    ui.key("DOWN")
                ui.key("ENTER")
                for _ in range(2):
                    ui.key("DOWN")
                ui.key("SPACE")
                for _ in range(3):
                    ui.key("DOWN")
                ui.key("ENTER")
                ui.text("The /32 is the most specific matching prefix.")
                ui.key("E")  # A command key while typing must not open evidence.
                self.assertIsNone(ui.modal)
                ui.key("ENTER")
                ui.key("DOWN")
                ui.key("ENTER")
                self.assertEqual(game.progress["stage"], "feedback")
                self.assertTrue(game.visible()["last"]["result"]["correct"])
                ui.key("V")
                self.assertIn("YOUR PREDICTION", ui.modal)
                self.assertIn("10.0.20.40/32", feedback_text(game.visible()))
                resumed = save.load()
                self.assertEqual(resumed.state, game.state)
                ui.key("ESCAPE")
                ui.key("ENTER")
                ui.focus = len(ui.rows()) - 2
                ui.key("ENTER")
                ui.text("Unfinished prediction survives window close.")
                ui.close()
                self.assertTrue(ui.quit)
                self.assertEqual(save.load().progress["draft"]["reason"], "Unfinished prediction survives window close.")

    def test_saved_progress_cannot_skip_decisions(self):
        game = Game()
        game.start("sorting")
        game.progress["index"] = 2
        with self.assertRaisesRegex(ValueError, "unfinished decision"):
            game.validate()

    def test_post_lesson_gates_read_reviews_without_mutation(self):
        game = Game()
        with self.assertRaisesRegex(ValueError, "post-lesson"):
            game.start("crumbs")
        self.assertIsNone(game.visible())
        with patch("packet_post.content.delivery.session_status", return_value={"reviews": {
            "c05.review": {"self": {"valid_pass": True}},
            "c06.review": {"self": {"valid_pass": True}},
            "exit.review": {"self": {"valid_pass": False}},
        }}), patch("packet_post.content.delivery.act") as mutate:
            game.authorize("completed")
            game.start("crumbs")
            game.begin()
            with self.assertRaises(ValueError):
                game.inspect("endpoint")
            with self.assertRaises(ValueError):
                game.start("recovery")
            mutate.assert_not_called()
        self.assertNotIn("endpoint", game.progress["opened"])

    def test_handoff_hides_case_before_prediction_and_uses_new_ids(self):
        game = Game()
        game.start("handoff")
        game.begin()
        self.assertEqual(game.visible()["scene"]["cards"], [])
        with self.assertRaises(ValueError):
            game.inspect("practice-cases")
        game.commit(dict(hypotheses=["routing or policy changed", "application unavailable"]), "request state to distinguish")
        game.advance()
        case = game.inspect("practice-cases")
        self.assertIn("P1-1", case)
        self.assertNotIn("case-a.json", case)

    def test_all_missions_can_complete_without_awarding_course_credit(self):
        game = Game()
        game.reviewed = {"c05.review", "c06.review", "exit.review"}
        for mission in content.missions():
            game.start(mission["id"])
            game.begin()
            for step in mission["steps"]:
                scene = content.scenes()[step]
                values = {f["key"]: scene.expected[f["key"]].split(", ") if f.get("multiple") else scene.expected[f["key"]]
                          for f in scene.fields}
                game.commit(values, "Authored verification journey, not learner evidence.")
                self.assertTrue(game.visible()["last"]["result"]["correct"], step)
                game.advance()
            game.reflect(dict(mechanism="Rule explained", evidence="Named source", uncertainty="Scope unproved", action="Owner validates service"))
            self.assertEqual(game.progress["stage"], "complete")
        game.validate()
        self.assertEqual(len(game.state["stamps"]), len(content.missions()))
        self.assertNotIn("completion", game.state)

    def test_parcel_controls_change_real_bounded_result(self):
        scene = content.scenes()["parcel.plain"]
        fits = content.evaluate(scene, dict(payload="1160", fits="yes", maximum="1160 bytes"))
        too_big = content.evaluate(scene, dict(payload="1161", fits="no", maximum="1160 bytes"))
        self.assertTrue(fits["correct"])
        self.assertTrue(too_big["correct"])
        self.assertEqual(fits["model"]["packet_bytes"], 1200)
        self.assertFalse(too_big["model"]["fits"])
        self.assertEqual(content.scenes()["parcel.tcp-options"].expected["maximum"], "1148 bytes")
        self.assertEqual(content.scenes()["parcel.ip-options"].expected["maximum"], "1144 bytes")

    def test_budget_accepts_different_pairs_and_keeps_risks(self):
        scene = content.scenes()["budget.state"]
        first = content.evaluate(scene, dict(options=["state-sync", "monitoring"], recovered="no"))
        second = content.evaluate(scene, dict(options=["backup-path", "management"], recovered="no"))
        self.assertTrue(first["correct"] and second["correct"])
        self.assertNotEqual(first["model"]["addressed_dependencies"], second["model"]["addressed_dependencies"])
        with self.assertRaises(ValueError):
            content.evaluate(scene, dict(options=["state-sync"], recovered="no"))
        twist = content.evaluate(content.scenes()["budget.twist"], dict(options=["backup-path", "management"], recovered="no"))
        self.assertTrue(any("share building power" in v for v in twist["model"]["residual_risk"]))

    def test_route_choices_and_boundaries(self):
        scenes = content.scenes()
        self.assertEqual(scenes["route.host"].expected, dict(prefix="10.0.20.40/32", hops="10.0.10.252"))
        self.assertEqual(scenes["route.remove"].expected, dict(prefix="10.0.20.0/24", hops="10.0.10.253, 10.0.10.254"))
        self.assertEqual(scenes["route.vrf"].expected, dict(corp="0.0.0.0/0", ot="no route"))
        incomplete = content.evaluate(scenes["route.remove"], dict(prefix="10.0.20.0/24", hops=["10.0.10.253"]))
        self.assertFalse(incomplete["correct"])
        self.assertIn("Policy enforcement", incomplete["unknowns"])

    def test_commit_reveal_retry_and_duplicate_confirm(self):
        game = Game()
        game.start("sorting")
        game.begin()
        before = copy.deepcopy(game.state)
        with self.assertRaises(ValueError):
            game.commit({}, "a prediction")
        self.assertEqual(game.state, before)
        self.assertNotIn("expected", game.visible()["scene"])
        self.assertNotIn("last", game.visible())
        game.commit(dict(prefix="10.0.0.0/8", hops=["10.0.10.254"]), "try a covering route")
        with self.assertRaises(ValueError):
            game.commit(dict(prefix="10.0.0.0/8", hops=["10.0.10.254"]), "duplicate")
        self.assertFalse(game.visible()["last"]["supported"])
        game.retry()
        game.commit(dict(prefix="10.0.20.40/32", hops=["10.0.10.252"]), "longest match")
        self.assertTrue(game.visible()["last"]["supported"])
        self.assertEqual(len(game.progress["attempts"]["route.host"]), 2)
        game.advance()
        self.assertNotIn("last", game.visible())

    def test_hint_and_evidence_are_durable_without_course_credit(self):
        game = Game()
        game.start("sorting")
        game.begin()
        with self.assertRaises(ValueError):
            game.inspect("case.exit")
        game.inspect("routes")
        game.hint()
        game.commit(dict(prefix="10.0.20.40/32", hops=["10.0.10.252"]), "matching host route")
        with tempfile.TemporaryDirectory() as temp:
            with Save("test", Path(temp)) as save:
                save.write(game)
                resumed = save.load()
                self.assertEqual(resumed.state, game.state)
                self.assertTrue(resumed.visible()["last"]["supported"])
                first, second = save.export(game), save.export(game)
                self.assertNotEqual(first, second)
                self.assertIn("no course attainment", first.read_text())
                with self.assertRaisesRegex(ValueError, "another Packet Post"):
                    with Save("test", Path(temp)):
                        pass

    def test_failed_write_and_bad_load_preserve_original(self):
        with tempfile.TemporaryDirectory() as temp:
            with Save("test", Path(temp)) as save:
                game = Game()
                save.write(game)
                path = save.path / "state.json"
                original = path.read_bytes()
                game.start("sorting")
                with patch("packet_post.game.os.replace", side_effect=OSError("disk full")):
                    with self.assertRaises(OSError):
                        save.write(game)
                self.assertEqual(path.read_bytes(), original)
                path.write_text('{"truncated":')
                with self.assertRaisesRegex(ValueError, "Original kept"):
                    save.load()
                self.assertEqual(path.read_text(), '{"truncated":')
                state = json.loads(original)
                state["content_sha256"] = "changed"
                path.write_text(json.dumps(state))
                with self.assertRaisesRegex(ValueError, "different game/content"):
                    save.load()

    def test_directory_confinement(self):
        with tempfile.TemporaryDirectory() as temp:
            for ident in ("../escape", "", "Bad", "a/b"):
                with self.assertRaises(ValueError):
                    Save(ident, Path(temp))
            occupied = Path(temp) / "occupied"
            occupied.mkdir()
            with self.assertRaisesRegex(ValueError, "not a Packet Post"):
                with Save("occupied", Path(temp)):
                    pass
            (Path(temp) / "link").symlink_to(occupied, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic"):
                Save("link", Path(temp))


if __name__ == "__main__":
    unittest.main()
