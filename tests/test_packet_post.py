"""Practice correctness and recovery, without tcod or a display."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from packet_post import content
from packet_post.game import Game, Save


class PacketPostTests(unittest.TestCase):
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
