"""Focused, offline verification of evidence claims in published case studies.

Keeps public synthetic-case summaries aligned with frozen JSON expectations and
underlying source constants. Does not repeat Python security-lab tests.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def required(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    net = json.loads(get("projects/03-network-pcap/expected_findings.json"))
    reqs = net["findings"]
    required(net["packet_count"] == 20 and net["decoded_event_count"] == 12,
             "Network fixture counts changed; review public case")
    required(len(reqs) == 2 and {x["rule_id"] for x in reqs} ==
             {"NET_DNS_NXDOMAIN_BURST", "NET_HTTP_POST_RESERVED_HOST"},
             "Network expected finding IDs changed")
    net_doc = get("projects/03-network-pcap/CASE_REPORT.md")
    net_html = get("projects/network-traffic-analysis.html")
    for finding in reqs:
        for key in ("rule_id", "observed_at_utc"):
            required(finding[key] in net_doc,
                     f"Network report missing expected {key}: {finding[key]}")
    for value in ("LAB-NET-001", "Four", "POST"):
        required(value.lower() in net_html.lower(),
                 f"Network rendered case missing {value}")
    required("projects/03-network-pcap/CASE_REPORT.md" in net_html,
             "Network page no longer links to GitHub-rendered report")

    web = json.loads(get("projects/04-local-vulnerability-assessment/expected_assessment.json"))
    required(len(web["expected_before_findings"]) == 4 and not web["expected_after_findings"],
             "Web hardening expected finding counts changed")
    web_doc = get("projects/04-local-vulnerability-assessment/CASE_REPORT.md")
    web_html = get("projects/vulnerability-remediation.html")
    for rule in web["expected_before_findings"]:
        required(rule in web_doc, f"Web case report missing rule identifier: {rule}")
    required("LAB-WEB-001" in web_html and
             "projects/04-local-vulnerability-assessment/CASE_REPORT.md" in web_html,
             "Web page missing case ID or full rendered evidence link")
    # The Stage B in-memory Splunk data must exactly match the canonical CSV.
    # This verifies fixture integrity; it does not execute Splunk.
    import csv
    import re
    from io import StringIO
    matrix_csv = get("projects/01-authentication-detection/validation_events.csv")
    rows = list(csv.DictReader(StringIO(matrix_csv)))
    required(len(rows) == 64 and len({r["scenario"] for r in rows}) == 9,
             "Authentication corpus drifted from 64 records / nine scenarios")
    keys = ("timestamp", "username", "source_ip", "host", "event_type", "scenario")
    expected_payload = ";".join("|".join(row[k] for k in keys) for row in rows)
    full_spl = get("projects/01-authentication-detection/SPLUNK_MATRIX_IN_MEMORY.spl")
    match = re.search(r'(?m)^\| eval fixture_rows="([^"]+)"$', full_spl)
    required(match is not None and match.group(1) == expected_payload,
             "In-memory SPL fixture differs from the authoritative CSV")
    required("fixture_event_count" in full_spl
             and "fixture_scenario_count" in full_spl
             and "streamstats time_window=10m" in full_spl,
             "Stage B SPL lacks fixture counters or windowed detection")
    evidence = get("projects/01-authentication-detection/SPLUNK_SMOKE_OBSERVATION_2026-10-23.md")
    required("64-event" in evidence and "PENDING" in evidence
             and "has not been committed" in evidence,
             "Screenshot review must not imply complete 64-event verification")

    # The candidate retest uses precisely the same 64 source rows and
    # an explicit inclusive 0..600 second comparison (not a wider window).
    candidate = get("projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST.spl")
    candidate_match = re.search(r'(?m)^\| eval fixture_rows="([^"]+)"$', candidate)
    required(candidate_match is not None and candidate_match.group(1) == expected_payload,
             "Boundary retest fixture differs from the frozen 64-event source")
    for token in ("streamstats current=f list(failure_epoch)",
                  "mvmap(prior_failure_times,_time-tonumber(prior_failure_times))",
                  "mvfilter(isnotnull(age_seconds) AND age_seconds>=0 AND age_seconds<=600)"):
        required(token in candidate, "Boundary candidate missing expected predicate: " + token)
    required("time_window=10m" not in candidate,
             "Boundary retest must not reuse the observed failing time-window term")
    failure_report = get("projects/01-authentication-detection/SPLUNK_MATRIX_FIRST_RUN_2026-10-23.md")
    required("3/5" in failure_report and "user_alpha" in failure_report
             and "user_boundary" in failure_report and "NOT PASSED" in failure_report,
             "Real Splunk mismatch record must preserve both missing detections")

    # Recruiter-facing landing page must expose all four fixture-backed reports
    # and must not silently omit pending Splunk/Wireshark status.
    home = get("index.html")
    landing = get("projects/soc-analyst-evidence.html")
    for report in (
        "01-authentication-detection/SOC_CASE_REPORT.md",
        "02-windows-process-triage/CASE_REPORT.md",
        "03-network-pcap/CASE_REPORT.md",
        "04-local-vulnerability-assessment/CASE_REPORT.md",
    ):
        required(report in home and report in landing,
                 f"Recruiter landing evidence link missing: {report}")
    required('id="soc-evidence"' in home and
             'href="projects/soc-analyst-evidence.html"' in home,
             "Homepage missing recruiter pathway")
    for term in ("Splunk", "Wireshark", "76", "synthetic"):
        required(term.lower() in landing.lower(),
                 f"Dedicated recruiter page missing qualification: {term}")

    for source in (net_doc, web_doc):
        required("not" in source.lower() and "synthetic" in source.lower(),
                 "Evidence boundary disclosure missing")

    print("PASS: 2 source-linked case reports, frozen rule IDs/times, and webpage links")
    print("Scope: static evidence consistency; not a live security assessment")


if __name__ == "__main__":
    main()
