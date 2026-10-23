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

    # Stage B2 screenshot-reviewed findings must remain tied to frozen expected rows,
    # while not asserting that query/SID or export provenance was obtained.
    reviewed = get("projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST_RESULT_2026-10-23.md")
    required("5/5" in reviewed and "cropped" in reviewed.lower()
             and "64" in reviewed and "job" in reviewed.lower(),
             "Stage B2 report must retain matching output and evidence limitations")
    for user in ("user_threshold", "user_reset", "user_boundary", "user_alpha", "user_beta"):
        required(user in reviewed, "Stage B2 observation missing expected account: " + user)
    # The new SOC integration package must stay visibly marked as pending real
    # dashboard and alert execution; source verification is not runtime proof.
    pack = get("splunk_workflow/README.md")
    required("PREPARED" in pack and "NOT YET VERIFIED" in pack
             and "disabled" in pack.lower() and "64" in pack,
             "Splunk app must retain synthetic/demo vs runtime evidence boundary")
    # Screenshot-reviewed native *one-panel* dashboard is separate from six-panel XML.
    native = get("splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md")
    required("ONE_PANEL_NATIVE_DASHBOARD_VERIFIED_BY_SCREENSHOT" in native
             and "not yet stored in this public repository" in native
             and "six-panel" in native and "real attack" in native,
             "Native dashboard evidence status or limitations drifted")
    for user in ("user_threshold", "user_reset", "user_boundary", "user_alpha", "user_beta"):
        required(user in native, "Native dashboard report missing source case " + user)
    # This public visual is a reproducible synthetic example, never a claimed
    # screenshot from Splunk or a real alert trigger.
    visual = get("projects/splunk-synthetic-preview.html")
    failed = sum(row["event_type"] == "login_failure" for row in rows)
    succeeded = sum(row["event_type"] == "login_success" for row in rows)
    for key, value in (("data-fixture-events", len(rows)),
                       ("data-fixture-failures", failed),
                       ("data-fixture-successes", succeeded),
                       ("data-fixture-scenarios", len({r["scenario"] for r in rows})),
                       ("data-expected-findings", 5)):
        required(f'{key}="{value}"' in visual,
                 "Simulated overview diverges from canonical fixture: " + key)
    required("Practice dataset" in visual
             and "Training example" in visual
             and "not exported from Splunk" in visual
             and "not an actual triggered Splunk alert" in visual
             and "splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md" in visual,
             "Visual preview must keep synthetic/real evidence boundaries explicit")
    for row in __import__("json").loads(get(
             "projects/01-authentication-detection/expected_findings.json"))["expected_findings"]:
        if row["username"] == "user_boundary":
            required(row["timestamp"] in visual and row["source_ip"] in visual,
                     "Illustrative alert must match the frozen oracle boundary case")

    # Feature only demonstrated Splunk scope; prevent stale "not run" homepage copy.
    home_v4 = get("index.html")
    required('id="featured-splunk"' in home_v4 and "3 / 5" in home_v4 and "5 / 5" in home_v4,
             "Homepage missing featured Splunk debugging evidence")
    required("Splunk execution still pending" not in home_v4
             and "have not been executed in Splunk" not in home_v4
             and "Splunk on-platform execution" not in home_v4,
             "Homepage contains obsolete pre-Splunk execution status")
    required("indexed ingestion and alerts not verified" in home_v4
             and "training events" in home_v4.lower()
             and "NATIVE_DASHBOARD_RESULT_2026-10-23.md" in home_v4,
             "Homepage must distinguish real Splunk UI evidence from untested deployment")
    project_slice = home_v4.split('id="projects"', 1)[1].split('id="evidence"', 1)[0]
    security_pos = [project_slice.find(s) for s in (
        "Authentication Detection", "Windows Process", "Network Traffic",
        "Vulnerability Assessment", "Celestial Resonance", "Research AI Infrastructure")]
    required(all(x >= 0 for x in security_pos) and security_pos == sorted(security_pos),
             "Security labs must precede private engineering case studies")
    # Resume/recruiter claims must remain grounded in completed screenshot review.
    onepage = get("docs/RECRUITER_QUICK_BRIEF.md")
    bullets = get("docs/RESUME_PORTFOLIO_BULLETS.md")
    required("64-event" in onepage and "5/5" in onepage
             and "not a public repository image artifact" in onepage,
             "Recruiter one-pager must disclose synthetic data and evidence provenance")
    required("Splunk Enterprise" in bullets and "5/5" in bullets
             and "actual Splunk execution remains pending" not in bullets,
             "Resume bullets drifted to unsupported or obsolete Splunk status")
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
