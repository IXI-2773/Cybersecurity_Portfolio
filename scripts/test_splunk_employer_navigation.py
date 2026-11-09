"""Focused, no-browser checks for the employer's investigation/evidence path."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CASE = "projects/soc-triage-automation.html"
EXCERPT = CASE + "#report-excerpt"


class Navigation(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.links, self.articles = [], [], []
        self.article = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "article":
            self.article = {"classes": attrs.get("class", "").split(), "links": []}
            self.articles.append(self.article)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
            if self.article is not None:
                self.article["links"].append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == "article":
            self.article = None


class EmployerNavigationTests(unittest.TestCase):
    def test_homepage_leads_with_investigation_without_adding_features(self):
        page = Navigation(ROOT / "index.html")
        features = [a for a in page.articles if "project-row" in a["classes"]]
        self.assertEqual(len(features), 3)
        self.assertIn(CASE, features[0]["links"])
        self.assertIn(EXCERPT, features[0]["links"])

    def test_each_case_summary_opens_the_investigation_and_readable_evidence(self):
        for name in ("index.html", "explore.html", "recruiter.html"):
            with self.subTest(page=name):
                page = Navigation(ROOT / name)
                summaries = [a for a in page.articles if CASE in a["links"]]
                self.assertEqual(len(summaries), 1)
                self.assertIn(EXCERPT, summaries[0]["links"])

    def test_modified_pages_local_navigation_resolves(self):
        for name in ("index.html", "explore.html", "recruiter.html"):
            page_path = ROOT / name
            page = Navigation(page_path)
            self.assertEqual(len(page.ids), len(set(page.ids)), name)
            for href in page.links:
                parsed = urlsplit(href)
                if parsed.scheme or parsed.netloc:
                    continue
                dest = (page_path.parent / unquote(parsed.path)).resolve() if parsed.path else page_path
                with self.subTest(page=name, href=href):
                    self.assertTrue(dest.is_file())
                    if parsed.fragment and dest.suffix == ".html":
                        self.assertIn(parsed.fragment, Navigation(dest).ids)

    def test_scheduled_alert_and_historical_fixture_remain_accessible(self):
        home = Navigation(ROOT / "index.html")
        self.assertIn("projects/splunk-execution-workflow.html", home.links)
        case = Navigation(ROOT / CASE)
        self.assertIn("fixture-walkthrough", case.ids)
        self.assertIn("10-soc-triage/artifacts/report.html", case.links)
        self.assertIn("../assets/evidence/soc-authentication-export-excerpt.json", case.links)


if __name__ == "__main__":
    unittest.main()
