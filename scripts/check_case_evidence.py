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
             and "cropped and resized derivative" in native
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

    # Employer navigation must expose the full reviewed catalog without scripts.
    import re
    home = get("index.html")
    required((ROOT / 'projects/e3-digital-forensics.html').exists(),
             "E3 classroom experience needs its own case")
    e3 = get('projects/e3-digital-forensics.html')
    required('data-case-scope="completed-reproducible-lab"' in e3
             and 'owner-confirmed tool experience' in e3.lower(),
             "Forensic case must separate reproducible evidence from E3 classroom experience")
    kali_vm = get('projects/kali-defender-visibility.html')
    required('data-case-scope="completed-owner-confirmed-experience"' in kali_vm,
             "Kali/VM case must present the owner-confirmed work as completed experience")
    for phrase in ('Completed hands-on experience', 'VMware', 'Wireshark', 'Snort', 'Splunk'):
        required(phrase.lower() in kali_vm.lower(),
                 "Kali/VM completed case missing experience marker: " + phrase)
    for stale in ('proposed walkthrough', 'has not been executed', 'design, not a newly completed'):
        required(stale not in kali_vm.lower(),
                 "Kali/VM completed case retained stale proposal wording: " + stale)
    required('Reproducible public artifact' in kali_vm
             and 'Attributed reference image' in kali_vm,
             "Kali/VM visuals must distinguish public artifacts from reference imagery")
    for asset in ('assets/reference/csusb-jack-brown-hall.webp',
                  'assets/reference/csusb-university-entrance.webp'):
        required((ROOT / asset).exists(), "Missing licensed CSUSB image: " + asset)
        required((ROOT / asset).stat().st_size <= 1024 * 1024,
                 "CSUSB image exceeds live response size ceiling: " + asset)
        required(asset in get('education.html'), "Academic gallery missing image: " + asset)
        required(asset in get('visual-credits.html'), "Image credits missing image: " + asset)
    required('class="campus-gallery"' in get('education.html'),
             "Academic experience needs the responsive campus gallery")
    required(home.count('https://github.com/IXI-2773"') == 1
             and home.count('https://www.linkedin.com/in/ixi2773/"') == 1,
             "Keep one prominent profile link for each social destination")
    catalog = get("explore.html")
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S)
    required(heading is not None and "Don Lopez" in heading.group(1),
             "Homepage must introduce Don Lopez directly")
    required("Cybersecurity Analyst" in home and 'href="explore.html"' in home
             and "Explore all work" in home,
             "Homepage needs a clear employer choice action")
    resume = "resumes/Don_Lopez_Cybersecurity_Resume.pdf"
    required(f'href="{resume}"' in home and (ROOT / resume).read_bytes().startswith(b"%PDF-"),
             "Primary resume must be the master-derived public PDF")
    cases = ("authentication-detection", "windows-process-triage", "network-traffic-analysis",
             "vulnerability-remediation", "phishing-investigation", "identity-mfa-investigation",
             "e3-digital-forensics", "offensive-security-vm-labs", "celestial-resonance",
             "research-ai-infrastructure", "certification-learning-engine")
    for slug in cases:
        required(f'href="projects/{slug}.html"' in catalog,
                 "Employer choice page missing case: " + slug)
        required(slug + ".html" in get("sitemap.xml"), "Case missing from sitemap: " + slug)
    required('href="roles.html"' in catalog, "Retain the existing role-based review choice")
    required("B.S. Information Systems" in home.split('<section class="work-section"')[0],
             "Degree must be visible in the opening introduction")
    for slug in ("detection-engineering", "splunk-siem-investigation", "network-intrusion-lab"):
        rendered = get("projects/" + slug + ".html")
        required('data-case-scope="resume-lab"' in rendered and "original" in rendered.lower(),
                 "Resume case must identify its evidence scope: " + slug)
        required(f'href="projects/{slug}.html"' in catalog, "Resume case missing from catalog: " + slug)
    for slug in ("soc-triage-automation",):
        rendered = get("projects/" + slug + ".html")
        required('data-case-scope="planned-project"' in rendered and "Not yet executed" in rendered,
                 "Planned brief must not claim completed work: " + slug)
        required(f'href="projects/{slug}.html"' in catalog, "Planned brief missing from catalog: " + slug)

    # Evidence expansion contract: completed cases provide inspectable artifacts.
    for slug, evidence_path in (
        ("phishing-investigation", "projects/05-phishing-email/CASE_REPORT.md"),
        ("identity-mfa-investigation", "projects/06-enterprise-account/CASE_REPORT.md"),
        ("vulnerability-remediation", "projects/04-local-vulnerability-assessment/access.log"),
        ("e3-digital-forensics", "projects/07-forensic-evidence/CASE_REPORT.md"),
    ):
        rendered = get("projects/" + slug + ".html")
        required('data-case-scope="completed-reproducible-lab"' in rendered,
                 "Expanded case must be completed and reproducible: " + slug)
        required(evidence_path in rendered,
                 "Expanded case missing direct evidence link: " + slug)
        required("Reproducible lab result" in rendered,
                 "Expanded case missing visual evidence label: " + slug)
    offensive = get("projects/offensive-security-vm-labs.html")
    for phrase in ("Owner-confirmed prior training", "Necromancer", "HackThisSite", "VMware"):
        required(phrase in offensive, "Offensive experience missing: " + phrase)
    required("https://www.vulnhub.com/entry/the-necromancer-1%2C154/" in offensive
             and "https://www.hackthissite.org/info/about" in offensive,
             "Offensive experience must cite official training sources")
    required("Dean’s List" in get("awards.html") and "Spring 2023" in get("awards.html")
             and "Fall 2024" in get("awards.html"), "Keep both transcript-supported honors")
    required((ROOT/'education.html').exists(), "Transcript coursework needs a readable academic page")
    for code in ('4210','4620','4910','5250','2410','2510'):
        required(code in get('education.html'), "Academic page missing reviewed course: "+code)
    for path in ROOT.rglob('*.html'):
        if '.git' not in path.parts:
            required('assets/artwork/' not in path.read_text(), "Generated artwork remains displayed: "+str(path))
    for slug in ("ad-attack-chain", "detection-engineering", "network-traffic-analysis"):
        required(f'href="projects/{slug}.html"' in home,
                 "Homepage missing selected investigation: " + slug)
    for slug in ("celestial-resonance", "research-ai-infrastructure"):
        case = get("projects/" + slug + ".html")
        required('data-case-scope="private-summary"' in case and "private" in case.lower(),
                 "Private engineering case must disclose its public scope: " + slug)
        required("https://github.com/IXI-2773/Celestial_Resonance" not in case
                 and "https://github.com/IXI-2773/Research-AI-Infrastructure" not in case,
                 "Private source URL must not enter public case")
    learning = get("projects/certification-learning-engine.html")
    for repo in ("Comptia-SY0-701-Test-Learning-Engine", "Microsoft_SC-900_Test_Learning_Engine"):
        required("https://github.com/IXI-2773/" + repo in learning,
                 "Study-engine case missing real source: " + repo)
    required("independent" in learning.lower() and "study" in learning.lower()
             and "guarantee" in learning.lower(),
             "Study-engine case must retain its independent study-tool scope")
    auth = get("projects/authentication-detection.html")
    required("64" in auth and "5 of 5" in auth and "synthetic" in auth.lower()
             and "indexed ingestion and alert firing" in auth.lower()
             and "not verified" in auth.lower()
             and "SPLUNK_MATRIX_BOUNDARY_RETEST.spl" in auth
             and "NATIVE_DASHBOARD_RESULT_2026-10-23.md" in auth,
             "Authentication case must retain source evidence and runtime limits")
    required('src="../assets/evidence/splunk-native-dashboard-results.png"' in auth
             and "cropped" in auth.lower(), "Keep the actual scoped Splunk image")
    for path in ("index.html", "explore.html", "projects/certification-learning-engine.html"):
        public = get(path)
        required("Brandon" not in public and "tel:" not in public,
                 "Public page exposed private master-resume details: " + path)
    for path in ("index.html", "explore.html"):
        required("CompTIA" in get(path) or "Security+" in get(path) or "case" in get(path).lower(),
                 "Employer page lost its professional context")
    reconciliation = get("docs/RESUME_SOURCE_RECONCILIATION_2026-10-23.md")
    required("5,000" in reconciliation and "20-frame" in reconciliation
             and "not independently verified" in reconciliation.lower(),
             "Keep broader resume projects distinct from public training fixtures")
    for path in ("resumes/Don_Lopez_SOC_Analyst.txt", "resumes/Don_Lopez_Security_Analyst.txt"):
        legacy = get(path)
        required("PORTFOLIO LABS, NOT EMPLOYMENT" in legacy and "Planned" in legacy,
                 "Legacy resume must preserve experience and certification scope")
    print("PASS: source evidence, employer case destinations, public resume and claim boundaries")
    print("Scope: static evidence consistency; not a live security assessment")


if __name__ == "__main__":
    main()
