from __future__ import annotations

import copy
import unittest

from evidence_visuals import render_case_visual, validate_summary


VALID = {
    "case_id": "LAB-TEST-001",
    "title": "Evidence <review>",
    "status": "Completed & reproducible",
    "metrics": [
        {"label": "Artifacts", "value": "4"},
        {"label": "Findings", "value": "2"},
    ],
    "timeline": [
        {"time": "09:00", "label": "Collected", "state": "observed"},
        {"time": "09:05", "label": "Analyzed", "state": "finding"},
    ],
    "findings": [
        {"id": "F-01", "label": "Reply-To mismatch", "severity": "high"},
    ],
}


class EvidenceVisualTests(unittest.TestCase):
    def test_rejects_missing_required_key(self) -> None:
        broken = copy.deepcopy(VALID)
        broken.pop("timeline")
        with self.assertRaisesRegex(ValueError, "timeline"):
            validate_summary(broken)

    def test_rejects_invalid_nested_shape(self) -> None:
        broken = copy.deepcopy(VALID)
        broken["metrics"][0].pop("value")
        with self.assertRaisesRegex(ValueError, "metrics"):
            validate_summary(broken)

    def test_render_is_deterministic_and_accessible(self) -> None:
        first = render_case_visual(VALID)
        second = render_case_visual(copy.deepcopy(VALID))
        self.assertEqual(first, second)
        self.assertIn('role="img"', first)
        self.assertIn('<title id="case-title">', first)
        self.assertIn('<desc id="case-desc">', first)
        self.assertIn("LAB-TEST-001", first)

    def test_render_escapes_untrusted_text_and_has_no_active_content(self) -> None:
        visual = render_case_visual(VALID)
        self.assertIn("Evidence &lt;review&gt;", visual)
        self.assertIn("Completed &amp; reproducible", visual)
        self.assertNotIn("<script", visual.lower())
        active_surface = visual.replace('xmlns="http://www.w3.org/2000/svg"', "")
        self.assertNotIn("href=", active_surface.lower())
        self.assertNotIn("http://", active_surface.lower())
        self.assertNotIn("https://", active_surface.lower())


if __name__ == "__main__":
    unittest.main()
