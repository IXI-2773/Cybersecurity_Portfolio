"""Focused navigation and provenance checks for the firewall case study."""

import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SNAPSHOT = "1713679893149ec90abb21c8fa1b3c63d3798660"
RANGE_SNAPSHOT = "6cdacdbfbe8adb7e38bd370b95b8793b4edd5ab9"
RANGE_REPORT = "projects/firewall-policy-review/artifacts/port_range_overlap_report.html"


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


class ReportRows(HTMLParser):
    """Read the evidence cells a visitor sees, including decoded HTML entities."""

    def __init__(self):
        super().__init__()
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.row = []
        elif tag == "td":
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row:
            self.rows.append(self.row)
            self.row = None


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

    def test_case_opens_separate_range_evidence_snapshot(self):
        links = links_in("projects/firewall-policy-review.html")
        self.assertIn("firewall-policy-review/artifacts/port_range_overlap_report.html", links)
        for artifact in (
            "fixtures/iptables_port_range_overlap.rules",
            "artifacts/port_range_overlap_report.json",
            "artifacts/port_range_overlap_report.csv",
            "artifacts/port_range_disjoint_report.json",
            "artifacts/port_range_execution.json",
        ):
            with self.subTest(artifact=artifact):
                self.assertIn(
                    f"https://github.com/IXI-2773/Cybersecurity-Projects/blob/{RANGE_SNAPSHOT}/projects/13-firewall-policy-review/{artifact}",
                    links,
                )

    def test_range_report_preserves_order_and_exact_overlap_witness(self):
        path = ROOT / RANGE_REPORT
        self.assertTrue(path.is_file(), "The range example needs a browsable saved report")
        parser = ReportRows()
        parser.feed(path.read_text(encoding="utf-8"))
        self.assertEqual(len(parser.rows), 1)
        self.assertEqual(parser.rows[0][:3], ["INFO", "INPUT:L5", "PARTIALLY_SHADOWED_RULE"])
        self.assertEqual(
            parser.rows[0][4:],
            ["INPUT:L4", "10.0.0.128/25 → 0.0.0.0/0 (tcp/85:90)"],
        )

    def test_range_report_returns_to_case_and_original_artifact(self):
        self.assertTrue((ROOT / RANGE_REPORT).is_file())
        links = links_in(RANGE_REPORT)
        self.assertIn("../../firewall-policy-review.html#port-ranges", links)
        self.assertIn(
            f"https://github.com/IXI-2773/Cybersecurity-Projects/blob/{RANGE_SNAPSHOT}/projects/13-firewall-policy-review/artifacts/port_range_overlap_report.html",
            links,
        )


if __name__ == "__main__":
    unittest.main()
