"""Focused navigation and provenance checks for the firewall case study."""

import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SNAPSHOT = "1713679893149ec90abb21c8fa1b3c63d3798660"


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def links_in(path):
    parser = Anchors()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    return parser.hrefs


class FirewallCaseNavigationTests(unittest.TestCase):
    def test_employers_can_reach_case_from_main_entrypoints(self):
        for page in ("index.html", "explore.html", "recruiter.html"):
            with self.subTest(page=page):
                self.assertIn("projects/firewall-policy-review.html", links_in(page))

    def test_case_links_to_source_walkthrough_and_report(self):
        page = "projects/firewall-policy-review.html"
        links = links_in(page)
        self.assertIn("firewall-policy-review/artifacts/partial_overlap_report.html", links)
        self.assertTrue(any(SOURCE_SNAPSHOT in url and url.endswith("/CASE_STUDY.md") for url in links))
        self.assertTrue(any(SOURCE_SNAPSHOT in url and "/tree/" in url for url in links))
        self.assertTrue(any(SOURCE_SNAPSHOT in url and url.endswith("/artifacts/partial_overlap_restricted_report.json") for url in links))

        text = (ROOT / page).read_text(encoding="utf-8").lower()
        self.assertIn("synthetic", text)
        self.assertIn("no live firewall", text)

    def test_saved_report_is_browsable(self):
        path = ROOT / "projects/firewall-policy-review/artifacts/partial_overlap_report.html"
        text = path.read_text(encoding="utf-8")
        self.assertIn("UNRESTRICTED_ADMIN_SOURCE", text)
        self.assertIn("PARTIALLY_SHADOWED_RULE", text)


if __name__ == "__main__":
    unittest.main()
