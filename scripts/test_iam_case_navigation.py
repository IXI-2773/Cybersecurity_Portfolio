"""Focused employer navigation and traceability checks for the IAM case."""

import unittest

from test_firewall_case_navigation import ROOT, links_in


SOURCE_SNAPSHOT = "b991e1599cae3dc4a4f8588e33e0af46a3352d73"
CASE_PAGE = "projects/iam-policy-review.html"


class IamCaseNavigationTests(unittest.TestCase):
    def test_employers_find_iam_case_from_primary_entrypoints(self):
        for page in ("index.html", "explore.html", "recruiter.html"):
            with self.subTest(page=page):
                self.assertIn(CASE_PAGE, links_in(page))

    def test_case_opens_source_study_and_both_saved_results(self):
        links = links_in(CASE_PAGE)
        self.assertTrue(any(SOURCE_SNAPSHOT in url and "/tree/" in url for url in links))
        for artifact in ("CASE_STUDY.md", "assumerole_broad_report.json", "assumerole_restricted_report.json"):
            with self.subTest(artifact=artifact):
                self.assertTrue(any(SOURCE_SNAPSHOT in url and url.endswith("/" + artifact) for url in links))

    def test_case_does_not_claim_real_cloud_access_or_validated_least_privilege(self):
        text = (ROOT / CASE_PAGE).read_text(encoding="utf-8").lower()
        self.assertIn("synthetic", text)
        self.assertIn("no aws account", text)
        self.assertIn("conditions", text)
        self.assertIn("not", text)


if __name__ == "__main__":
    unittest.main()
