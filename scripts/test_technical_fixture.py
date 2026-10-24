import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from build_technical_fixture import build_fixture, render, DEST, ROOT

class TechnicalFixtureTests(unittest.TestCase):
    def test_authentication_is_canonical(self):
        fixture = build_fixture()['authentication']
        with (ROOT/'projects/01-authentication-detection/validation_events.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),len(fixture['events']))
        for row,event in zip(rows,fixture['events']):
            self.assertEqual(row,{k:event[k] for k in row})
        self.assertEqual(fixture['expectedFindings'],json.loads((ROOT/'projects/01-authentication-detection/expected_findings.json').read_text())['expected_findings'])
        self.assertEqual(fixture['sourceHash'],hashlib.sha256((ROOT/'projects/01-authentication-detection/validation_events.csv').read_bytes()).hexdigest())
        self.assertIn('age_seconds<=600', fixture['splExcerpt'])
    def test_checked_in_output_is_current(self):
        self.assertEqual(DEST.read_text(),render())
    def test_stale_generated_output_rejected(self):
        original=DEST.read_bytes()
        try:
            DEST.write_text('stale')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/build_technical_fixture.py'),'--check'],capture_output=True)
            self.assertNotEqual(result.returncode,0)
        finally:
            DEST.write_bytes(original)

if __name__=='__main__': unittest.main()
