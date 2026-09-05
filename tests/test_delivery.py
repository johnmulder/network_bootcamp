"""Contracts and journeys for local course delivery."""

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import delivery as d


class DefinitionTests(unittest.TestCase):
    def test_definition_and_schedule(self):
        data = d.definition()
        self.assertEqual(sum(block["minutes"] for block in data["blocks"]), 360)
        self.assertEqual(sum(block["break_after"] for block in data["blocks"]), 60)
        for mutate in (
            lambda value: value["phases"][1].update(id=value["phases"][0]["id"]),
            lambda value: value["phases"][0].update(prerequisites=["exit.feedback"]),
            lambda value: value["phases"][0].update(minutes=200),
            lambda value: next(p for p in value["phases"] if p["id"] == "c02.inspect").update(evidence=["shell"]),
            lambda value: next(p for p in value["phases"] if p["id"] == "c02.calculate").update(checkpoints=["missing"]),
        ):
            changed = copy.deepcopy(data)
            mutate(changed)
            with self.assertRaises(d.DeliveryError):
                d.validate_definition(changed)

    def test_fragment_boundaries_and_bad_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "brief.md"
            path.write_text("<!-- delivery:start first -->\nQuestion\n<!-- delivery:end first -->\nSecret\n")
            self.assertEqual(d.fragments(path), {"first": "Question"})
            for text in (
                "<!-- delivery:start first -->\n<!-- delivery:start nested -->",
                "<!-- delivery:end missing -->",
                "<!-- delivery:start missing -->",
                "<!-- delivery:start a -->\n<!-- delivery:end a -->\n<!-- delivery:start a -->",
            ):
                path.write_text(text)
                with self.assertRaises(d.DeliveryError):
                    d.fragments(path)
            with self.assertRaises(d.DeliveryError):
                d.confined(Path(temp), "../escape")
        with self.assertRaises(d.DeliveryError):
            d.read_fragment({"path": "challenges/02-the-transfer-that-stops.md", "fragment": "missing"})


if __name__ == "__main__":
    unittest.main()
