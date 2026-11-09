"""Focused checks for the public, source-derived SOC excerpt and its links."""
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'projects/soc-triage-automation.html'
DATA = ROOT / 'assets/evidence/soc-authentication-export-excerpt.json'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.rows, self.row = [], [], [], None
        self.feed(text)

    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'tr' and 'data-source-ref' in a:
            self.row = {'ref': a['data-source-ref'], 'text': '', 'time': None}
        if tag == 'time' and self.row is not None:
            self.row['time'] = a.get('datetime')

    def handle_data(self, data):
        if self.row is not None:
            self.row['text'] += data

    def handle_endtag(self, tag):
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None


class PublicCaseTests(unittest.TestCase):
    def excerpt(self):
        self.assertTrue(DATA.is_file(), 'Public-safe excerpt is not installed')
        return json.loads(DATA.read_text())

    def test_provenance_and_counts_are_bound_to_observed_run(self):
        d = self.excerpt()
        self.assertEqual(d['source_case_sha256'], 'f7ff466a1919065bf8d904a691d16f93319dcba8359dea2e5c5f54708569f64b')
        self.assertEqual(d['implementation_commit'], 'c6519c1ecc04596e535a8f5079e4fa75334a0270')
        self.assertEqual(d['summary'], dict(input_rows=70, accepted_events=70, duplicate_rows=0, rejected_rows=0, review_candidates=6))

    def test_projection_contains_only_safe_fields_and_aliases(self):
        d = self.excerpt()
        self.assertEqual(set(d), {'schema','execution_date','data_origin','source_case_sha256','implementation_commit','summary','selection','privacy_transform','display_entities','candidate','events','scope'})
        self.assertEqual(d['display_entities'], dict(account='Account A', host='Host A', source='Source A'))
        self.assertEqual(set(d['candidate']), {'rule_id','timestamp_utc','window_seconds','source_refs'})
        for event in d['events']:
            self.assertEqual(set(event), {'timestamp_utc','event_type','source_refs'})
        for public_text in (json.dumps(d), PAGE.read_text()):
            self.assertNotRegex(public_text, r'[A-Za-z]:\\|/workspace/|DESKTOP-|sessionKey|scheduler__|(?:[0-9]{1,3}\.){3}[0-9]{1,3}')

    def test_selected_sequence_resolves_and_matches_authentication_rule(self):
        d = self.excerpt()
        events = d['events']
        self.assertEqual(len(events), 6)
        refs = [ref for event in events for ref in event['source_refs']]
        self.assertEqual(len(set(refs)), 6)
        self.assertEqual(refs, d['candidate']['source_refs'])
        for ref in refs:
            self.assertRegex(ref, r'^S[0-9]{2}:R[0-9]{6}$')
        self.assertEqual([e['event_type'] for e in events], ['login_failure'] * 5 + ['login_success'])
        times = [datetime.fromisoformat(e['timestamp_utc'].replace('Z', '+00:00')) for e in events]
        self.assertEqual(times, sorted(times))
        self.assertTrue(all(0 < (times[-1] - t).total_seconds() <= 600 for t in times[:-1]))
        self.assertEqual(events[-1]['timestamp_utc'], d['candidate']['timestamp_utc'])

    def test_visible_rows_match_public_source(self):
        d = self.excerpt()
        page = Page(PAGE.read_text())
        self.assertEqual(len(page.rows), 6)
        for row, event in zip(page.rows, d['events']):
            self.assertEqual(row['ref'], event['source_refs'][0])
            self.assertEqual(row['time'], event['timestamp_utc'])
            self.assertIn('Failure' if event['event_type'] == 'login_failure' else 'Success', row['text'])
            self.assertIn(row['ref'], row['text'])

    def test_report_navigation_distinguishes_excerpts_and_fixture_report(self):
        p = Page(PAGE.read_text())
        self.assertIn('report-excerpt', p.ids)
        self.assertIn('fixture-walkthrough', p.ids)
        self.assertIn('#report-excerpt', p.links)
        self.assertIn('../assets/evidence/soc-authentication-export-excerpt.json', p.links)
        self.assertIn('10-soc-triage/artifacts/report.html', p.links)
        self.assertEqual(len(p.ids), len(set(p.ids)))

    def test_local_links_and_anchors_resolve(self):
        p = Page(PAGE.read_text())
        for href in p.links:
            target = urlsplit(href)
            if target.scheme or target.netloc:
                continue
            dest = (PAGE.parent / unquote(target.path)).resolve() if target.path else PAGE
            self.assertTrue(dest.is_file(), href)
            if target.fragment and dest.suffix == '.html':
                self.assertIn(target.fragment, Page(dest.read_text()).ids, href)

    def test_historical_fixture_retains_partial_run_scope(self):
        page = PAGE.read_text()
        fixture = page.split('<h3 id="fixture-walkthrough">', 1)[1].split('</section>', 1)[0]
        self.assertIn('PARTIAL', fixture)
        self.assertIn('data-case-scope="completed-reproducible-tool"', fixture)


if __name__ == '__main__':
    unittest.main()
