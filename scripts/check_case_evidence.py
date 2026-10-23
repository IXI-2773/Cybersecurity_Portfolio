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

    # Project dossier structure: six consistent navigation bars, with private
    # architecture clearly distinct from testable public training fixtures.
    home_cards = get("index.html")
    required(home_cards.count('class="work-proofline"') == 4
             and home_cards.count('class="engineering-proofline"') == 2,
             "Four public-lab and two private architecture cards need matching proof labels")
    public_cases = (
        ("projects/authentication-detection.html", "scope-and-further-work"),
        ("projects/windows-process-triage.html", "scope-and-limits"),
        ("projects/network-traffic-analysis.html", "scope-and-limits"),
        ("projects/vulnerability-remediation.html", "scope-and-limits"),
    )
    private_cases = ("projects/celestial-resonance.html",
                     "projects/research-ai-infrastructure.html")
    for page, anchor in public_cases:
        source = get(page)
        required(source.count('class="case-review-strip"') == 1
                 and 'data-case-scope="public-lab"' in source
                 and f'href="#{anchor}"' in source
                 and 'class="case-review-actions"' in source,
                 "Public lab missing common review bar or scope anchor: " + page)
        required("Controlled evidence" in source
                 and "private implementation" not in source.split('class="case-review-strip"', 1)[1].split('class="article-layout"', 1)[0].lower(),
                 "Public lab review banner has incorrect disclosure: " + page)
    for page in private_cases:
        source = get(page)
        required(source.count('class="case-review-strip"') == 1
                 and 'data-case-scope="private-summary"' in source
                 and 'href="#public-scope"' in source
                 and 'Separate public' in source,
                 "Private case must label its independent teaching demonstration: " + page)
    for page in [p for p, _ in public_cases] + list(private_cases):
        source = get(page)
        required(source.index('class="case-snapshot"') < source.index('class="case-review-strip"')
                 < source.index('class="article-layout"'),
                 "Case review shortcuts must follow the summary and precede the report: " + page)
    # Shared recruiting tool design and real, connected interaction contracts.
    for page, active in (("explore.html", "explore"), ("test-lab.html", "lab"),
                         ("verify.html", "verify")):
        source = get(page)
        required(source.count('class="toolkit-masthead"') == 1
                 and source.count('class="toolkit-pipeline"') == 1,
                 "Tool page missing shared design system: " + page)
        required(source.count('data-toolkit-step=') == 3
                 and f'data-toolkit-step="{active}" aria-current="page"' in source,
                 "Tool page needs navigable and labeled active path: " + page)
    explorer = get("explore.html")
    required(explorer.count('data-quick-role=') == 4
             and 'class="explorer-role-pills"' in explorer,
             "Explorer needs all four functional role shortcuts")
    explorer_js = get("assets/js/explorer.js")
    required("button.dataset.quickRole" in explorer_js
             and "role.value = button.dataset.quickRole" in explorer_js
             and "aria-pressed" in explorer_js,
             "Explorer role shortcuts must update and announce filter state")
    lab = get("test-lab.html")
    required(lab.count('data-window-preset=') == 2
             and 'data-window-preset="599"' in lab
             and 'data-window-preset="600"' in lab,
             "Test lab needs both public authentication boundary presets")
    lab_script = get("assets/js/lab-ui.js")
    required("requestSubmit()" in lab_script
             and "updatePreset()" in lab_script
             and "button.dataset.windowPreset" in lab_script,
             "Lab presets must execute existing public engine and synchronize state")
    evidence_guide = get("verify.html")
    required(evidence_guide.count('class="verification-jump"') == 1
             and all(f'href="#{anchor}"' in evidence_guide for anchor in
                     ("public-lab-title", "engineering-title", "browser-title")),
             "Evidence guide must retain all three in-page scope links")
    # Four genuinely separate labs now have concise analyst-facing source
    # summaries, not a fabricated unified response case.
    briefs = (
        ("projects/authentication-detection.html", "64-event synthetic matrix",
         "validation_events.csv", "Expected findings", "SPLUNK_MATRIX_BOUNDARY_RETEST.spl"),
        ("projects/windows-process-triage.html", "two of five",
         "events_4688.csv", "CASE_REPORT.md", "process lineage"),
        ("projects/network-traffic-analysis.html", "20-frame PCAP",
         "generate_fixture.py", "CASE_REPORT.md", "Wireshark GUI"),
        ("projects/vulnerability-remediation.html", "four scoped fixture findings",
         "audit_demo.py", "CASE_REPORT.md", "Localhost-only"),
    )
    for page, finding, source_a, source_b, guardrail in briefs:
        public_case = get(page)
        required(public_case.count('class="case-analyst-brief"') == 1
                 and 'id="case-brief-title"' in public_case
                 and 'data-reviewed-case="public-lab"' in public_case
                 and public_case.count('class="case-brief-fact"') == 4
                 and public_case.count('data-brief-limit="true"') == 1,
                 "Public case must disclose question/observation/decision/limit: " + page)
        required(all(phrase.lower() in public_case.lower() for phrase in
                     (finding, source_a, source_b, guardrail)),
                 "Public case summary missing supported evidence and scope: " + page)
        required('href="#case-brief-title"' in public_case
                 and 'class="case-brief-details"' in public_case
                 and public_case.index('class="case-review-strip"')
                 < public_case.index('class="case-analyst-brief"')
                 < public_case.index('class="article-layout"'),
                 "Public case summary must lead to evidence without replacing report: " + page)
    guided = get("explore.html")
    required(guided.count('class="explorer-playbook"') == 1
             and guided.count('class="playbook-go"') == 4
             and "independent training scenarios" in guided
             and all(f'projects/{slug}.html#case-brief-title' in guided for slug in (
                 "authentication-detection", "windows-process-triage",
                 "network-traffic-analysis", "vulnerability-remediation")),
             "Guided analyst paths must link four separate, scoped cases")
    roles = get("roles.html")
    for target in ("soc-analyst", "security-analyst", "security-automation"):
        required(f'id="{target}"' in roles and f'href="#{target}"' in roles,
                 "Role page missing working role destination: " + target)
    required(roles.count('class="role-route-card"') == 3
             and roles.count('class="role-interview-question"') == 3
             and roles.count('class="role-scope"') == 3,
             "Each role needs a route, question and evidence limit")
    for case in ("projects/authentication-detection.html",
                 "projects/windows-process-triage.html",
                 "projects/network-traffic-analysis.html",
                 "projects/vulnerability-remediation.html",
                 "projects/celestial-resonance.html",
                 "projects/research-ai-infrastructure.html",
                 "test-lab.html#authentication-replay",
                 "test-lab.html#evidence-coverage"):
        required(case in roles, "Role page missing existing evidence path: " + case)
    required("independently authored" in roles.lower()
             and "private" in roles.lower()
             and "not" in roles.lower(),
             "Role page must retain limits of public/private evidence")
    required('href="roles.html"' in get("index.html")
             and 'href="roles.html"' in get("explore.html")
             and 'roles.html#security-automation' in get("apply.html"),
             "Homepage, explorer and application paths must all reach role guide")
    guide = get("verify.html")
    required(guide.count("data-evidence-card") == 7
             and guide.count('class="verification-limit"') == 7,
             "Evidence review guide must contain seven source/limit entries")
    for source in ("splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md",
                   "assets/evidence/splunk-native-dashboard-results.png",
                   "projects/03-network-pcap/CASE_REPORT.md",
                   "projects/04-local-vulnerability-assessment/CASE_REPORT.md"):
        required(source in guide, "Evidence review guide missing artifact: " + source)
    required("independently authored" in guide.lower()
             and "private" in guide.lower(),
             "Public teaching engines must remain distinct from private implementations")
    # Landing-page role clarity and genuine evidence must survive redesigns.
    hiring_home = get("index.html")
    import re as _hiring_re
    hiring_h1 = _hiring_re.search(r"<h1[^>]*>(.*?)</h1>", hiring_home,
                                  flags=_hiring_re.DOTALL | _hiring_re.IGNORECASE)
    required(bool(hiring_h1) and "SOC Analyst" in hiring_h1.group(1),
             "Homepage heading must identify target analyst role before scrolling")
    required('class="hero-evidence-image"' in hiring_home
             and 'src="assets/evidence/splunk-native-dashboard-results.png"' in hiring_home
             and "Actual cropped screenshot" in hiring_home
             and "Training data." in hiring_home
             and "no production incidents" in hiring_home,
             "Landing panel must show actual, scoped Splunk training evidence")
    required(hiring_home.index('id="featured-splunk"') <
             hiring_home.index('id="hiring-start"') <
             hiring_home.index('id="boundary-replay"'),
             "Source-first featured investigation should precede secondary recruiter routing")
    required(hiring_home.count('class="hero-evidence-image"') == 1
             and 'href="#featured-splunk">See the Splunk evidence' in hiring_home
             and 'href="recruiter.html">One-page profile' in hiring_home,
             "First-screen primary and secondary actions must match their destinations")
    required("B.S. Cybersecurity" in hiring_home
             and "holder-reported" in get("recruiter.html").lower(),
             "Portfolio must retain credential scope context")
    # Homepage boundary preview must use the verified browser engine, not
    # hardcoded substitute detections. The static labels are only expected rows.
    source = get("index.html")
    required('id="boundary-replay"' in source
             and 'assets/js/lab-data.js' in source
             and 'assets/js/test-engine.js' in source
             and 'assets/js/home-replay.js' in source,
             "Homepage boundary preview must reference public source/engine")
    required(source.count("data-replay-username=") == 5
             and source.count("data-replay-window=") == 2,
             "Homepage preview must expose five expected identities and two time windows")
    reference = json.loads(get("projects/01-authentication-detection/expected_findings.json"))
    expected_users = {row["username"] for row in reference["expected_findings"]}
    import re as _replay_re
    shown_users = set(_replay_re.findall(r'data-replay-username="([^"]+)"', source))
    required(shown_users == expected_users,
             "Homepage preview labels do not match the frozen expected finding identities")
    script = get("assets/js/home-replay.js")
    required("PortfolioEngine" in script and "PortfolioLabData" in script
             and "detectAuth" in script and "actual.has(key(reference))" in script
             and "seconds}-second inclusive" in script,
             "Homepage replay must calculate fixture findings using the public engine")
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
    # Focused recruiter journey contract: no falsely labeled download, readable
    # source reports, and direct role/resume/evidence navigation.
    required('href="recruiter.html">One-page profile' in home_v4,
             "Homepage must distinguish printable profile from an ATS résumé")
    required('class="hero-resume-download"' in home_v4
             and 'href="resumes/Don_Lopez_SOC_Analyst.txt"' in home_v4,
             "Homepage needs a direct SOC résumé download")
    required('href="roles.html"' in home_v4,
             "Homepage must expose the three-role hiring guide")
    onepage_html = get("recruiter.html")
    required('href="apply.html">Choose ATS résumé' in onepage_html,
             "Recruiter profile must not falsely label a link as a download")
    github_source = "https://github.com/IXI-2773/Cybersecurity_Portfolio/blob/main/"
    for name, document in (
        ("role paths", roles),
        ("evidence guide", guide),
        ("analyst workflow", get("projects/soc-analyst-workflow.html")),
    ):
        import re as _re
        raw_reports = _re.findall(r'href="(?!(?:https?://))[^"]+\.md(?:#[^"]*)?"', document)
        required(not raw_reports,
                 name + " has non-rendered relative Markdown links: " + repr(raw_reports))
    for report in ("splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md",
                   "projects/03-network-pcap/CASE_REPORT.md",
                   "projects/04-local-vulnerability-assessment/CASE_REPORT.md"):
        required(f'href="{github_source}{report}"' in guide,
                 "Review guide must open the readable GitHub source: " + report)
    # Resume/recruiter claims must remain grounded in completed screenshot review.
    onepage = get("docs/RECRUITER_QUICK_BRIEF.md")
    bullets = get("docs/RESUME_PORTFOLIO_BULLETS.md")
    required("64-event" in onepage and "5/5" in onepage
             and "cropped genuine Splunk dashboard screenshot" in onepage,
             "Recruiter one-pager must disclose synthetic data and evidence provenance")
    required("Splunk Enterprise" in bullets and "5/5" in bullets
             and "actual Splunk execution remains pending" not in bullets,
             "Resume bullets drifted to unsupported or obsolete Splunk status")
    # Employer-facing website profile must remain a sourced, honest resume
    # companion and never imply live production SOC employment.
    profile = get("recruiter.html")
    required("Splunk Enterprise Search &amp; Reporting" in profile
             and "3 of 5" in profile and "5 of 5" in profile
             and "64 synthetic events" in profile,
             "Recruiter profile must preserve the observed synthetic debugging case")
    required("Holder-reported" in profile and "cropped, size-reduced derivative is published" in profile
             and "Indexed CSV ingestion" in profile,
             "Recruiter profile must disclose credential and runtime limitations")
    required('href="recruiter.html"' in home_v4
             and "recruiter.html" in get("sitemap.xml"),
             "Recruiter profile must be reachable from homepage and sitemap")
    # Genuine operator evidence is a PNG asset; illustrative diagrams are
    # separately labeled and can never substitute for a Splunk screen capture.
    required('src="assets/evidence/splunk-native-dashboard-results.png"' in home_v4,
             "Homepage missing genuine Splunk screenshot image")
    auth = get("projects/authentication-detection.html")
    required('src="../assets/evidence/splunk-native-dashboard-results.png"' in auth,
             "Case study missing genuine Splunk screenshot")
    required('authentication-investigation-flow.svg' in auth
             and 'not a Splunk application screenshot' in auth,
             "Generated workflow must be labeled as an illustration")
    details = get("projects/soc-analyst-evidence.html")
    required('soc-evidence-pipeline.svg' in details
             and 'Workflow illustration' in details,
             "SOC evidence illustration must be separated from real screenshots")
    # ATS-friendly portfolio resume tracks must be genuinely source-backed.
    application = get("apply.html")
    required("id=\"soc-role\"" in application and "id=\"security-role\"" in application
             and "apply.html" in home_v4,
             "Application kit is not linked or role-specific")
    required('download="Don_Lopez_SOC_Analyst.txt"' in application
             and 'download="Don_Lopez_Security_Analyst.txt"' in application,
             "Downloadable text versions must remain available")
    for role_path in ("resumes/Don_Lopez_SOC_Analyst.txt",
                      "resumes/Don_Lopez_Security_Analyst.txt"):
        role = get(role_path)
        for fact in ("DON LOPEZ", "CompTIA Security+", "CompTIA CySA+",
                     "December 2024", "5 of 5"):
            required(fact in role, "Resume missing supported fact: " + role_path + " / " + fact)
        required("PORTFOLIO LABS, NOT EMPLOYMENT" in role
                 and "not invented" in role
                 and "https://github.com/IXI-2773/Cybersecurity_Portfolio" in role,
                 "Resume must preserve synthetic/employment boundary and evidence links")
        for prohibited in ("phone@example", "[your", "123-456", "Work Experience: SOC",
                           "SOC Analyst at ", "production incident resolved"):
            required(prohibited.lower() not in role.lower(),
                     "Resume has unsupported detail or placeholder: " + prohibited)
    application_doc = get("docs/APPLICATION_READINESS.md")
    required("actual employment history" in application_doc
             and "not a guarantee" in application_doc
             and "not established" in application_doc,
             "Application guide must give accurate contact/employment and ATS limitations")
    # Public release gates: do not automatically publish prior application contact
    # details or claim employer histories/verified issuer badges without evidence.
    gates = get("docs/PUBLICATION_GATES.md")
    cred = get("docs/CREDENTIALS.md")
    required("APPROVED FOR PUBLICATION" in gates and "NOT PUBLISHED" in gates
             and "NOT INVENTED" in gates and "frailtycraven@gmail.com" in gates,
             "Public contact approval and other withholding controls must both remain explicit")
    required("issued-to name" in cred and "Holder" not in cred[:100],
             "Credential disclosure or legal-name visibility guidance missing")
    required('id="application-status"' in application
             and "mailto:frailtycraven@gmail.com" in application
             and "GitHub profile" in application,
             "Application page missing approved email and professional profile")
    for role_path in ("resumes/Don_Lopez_SOC_Analyst.txt",
                      "resumes/Don_Lopez_Security_Analyst.txt"):
        role = get(role_path)
        required("Email: frailtycraven@gmail.com" in role
                 and "Public professional profile: https://github.com/IXI-2773" in role
                 and "Professional contact:" not in role,
                 "Resumes must show approved email separately from public GitHub profile")
    # Guard only approved public contact on the three submission entry points.
    for public_page in ("index.html", "recruiter.html", "apply.html"):
        page = get(public_page)
        required("mailto:frailtycraven@gmail.com" in page and "tel:" not in page,
                 "Public page missing approved email or discloses unapproved phone link")
        import re
        used = set(re.findall(r'mailto:([^"\\s<>?]+)', page))
        required(used == {"frailtycraven@gmail.com"},
                 "An unapproved alternate email was inserted into a public page")
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
