"""Learning contracts and independent checks of authored problems."""

import json
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
