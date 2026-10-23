# Cybersecurity Portfolio — Don Lopez

A public, static portfolio presenting **reproducible synthetic defensive security exercises** alongside **high-level case studies of private engineering work**.

## Hiring-team tools

The [project explorer](https://ixi-2773.github.io/Cybersecurity_Portfolio/explore.html) filters the six case studies and public verification workbench by role and skill. All entries and evidence links remain readable without JavaScript.

The [verification workbench](https://ixi-2773.github.io/Cybersecurity_Portfolio/test-lab.html) runs two independent browser teaching engines: authentication replay over the existing 64-event fixture, and structured attributed-evidence coverage. Nine executable baseline checks and negative controls produce real calculated results. A receipt download records fixture SHA-256 values and completed runs. These are separate from private CR/RAI implementations, the Python suite, and Splunk execution.

Reproduce the public engine checks: `python scripts/build_browser_fixture.py --check` and `node scripts/test_browser_engine.cjs`.

## Homepage refresh

The recruiter-focused homepage combines four visual public-lab cards, the genuine Splunk screenshot, compact engineering summaries, a direct SOC resume download, and keyboard-expandable evidence tables. Native HTML and scoped CSS keep the site dependency-free.

## Live portfolio website

**[Visit the fully rendered cybersecurity portfolio](https://ixi-2773.github.io/Cybersecurity_Portfolio/)**. The [CR case study](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/celestial-resonance.html) and [vulnerability remediation](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/vulnerability-remediation.html) now have a successful GitHub Pages deployment. The published website is separate from GitHub's source-code view.

## Open the case studies right now

**[View all six case studies in GitHub's readable format](projects/CASE_STUDIES.md).** This is the best option when browsing the repository; those pages display normally instead of exposing HTML source.

For an **offline backup of the designed site**, download the **`cybersecurity-portfolio-site` artifact** from the [latest successful GitHub Actions run](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions), extract `cybersecurity-portfolio-site.zip`, and open `index.html` in your browser. The ZIP is automatically generated and validated in CI; no Python installation is required to view the extracted HTML.

## Website versus source code

GitHub Pages is **enabled**, and GitHub has reported a successful build and deployment. Use the [live site](https://ixi-2773.github.io/Cybersecurity_Portfolio/) to view the styled HTML. The GitHub Code tab displays the *source* of `.html` files instead of rendering them; for code-hosted reading use the [Markdown case studies](projects/CASE_STUDIES.md).

Automated deployment health checks are defined in [`check-live-pages.yml`](.github/workflows/check-live-pages.yml) and run independently of the Python project tests; a passing source CI is not itself a proof that a public HTTP endpoint responded.

## Certifications

- **CompTIA Security+** — credential reported by the portfolio owner.
- **CompTIA CySA+** — credential reported by the portfolio owner.

Public badge URLs, exam versions, dates and renewal status have not been supplied. See the [credential record](docs/CREDENTIALS.md) for claim limits.

## Public profile and verification policy

The [publication readiness record](docs/PUBLICATION_GATES.md) reflects the owner's explicit approval to publish **frailtycraven@gmail.com** as the professional contact. Other email addresses, phone numbers, unverified employment chronology and issuer-backed badge URLs remain unpublished.

## Role-targeted job application materials

[Open the application toolkit](https://ixi-2773.github.io/Cybersecurity_Portfolio/apply.html) to download **two ATS-oriented plain-text résumé drafts** and review interviewer evidence prompts. The SOC Analyst and Security Analyst versions contain the approved professional email, owner-reported credentials and source-backed lab work, without invented phone numbers, employment or production incidents. [Tailoring checklist](docs/APPLICATION_READINESS.md).

## Recruiter-ready web profile

[View the print-friendly, one-page SOC Analyst profile](https://ixi-2773.github.io/Cybersecurity_Portfolio/recruiter.html). It presents the verified Splunk 3/5 → 5/5 case, credentials as owner-reported, and three additional source-linked security investigations; browser print can save it as PDF. It includes the approved professional email and excludes invented employers, phone numbers and operational incident claims.

## One-page recruiter evidence brief

[Review Don Lopez's SOC Analyst evidence brief](docs/RECRUITER_QUICK_BRIEF.md) — a concise, source-linked summary of the screenshot-reviewed Splunk debugging result, all four public labs, qualification limits and interview evidence.

## Featured Splunk authentication investigation

The [live homepage](https://ixi-2773.github.io/Cybersecurity_Portfolio/#featured-splunk) now leads with the **3/5 → 5/5** ten-minute boundary debugging case and a saved Splunk dashboard table. [Operator screenshot observations](splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md) document the five matched synthetic cases. The on-site data table is a summary of observed screenshot results, not a new live product screenshot.

The source artifact and genuine result screenshot are distinct from the [CSV-derived charts](projects/splunk-synthetic-preview.html), which are practice-data visualizations.

## SOC authentication analysis visuals

[Explore SOC authentication charts and rule-based alert walkthrough](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/splunk-synthetic-preview.html). Figures come from the existing **64-event training dataset**; they are lab-generated, not Splunk exports or actual triggered alerts. Genuine [one-panel Splunk dashboard evidence](splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md) remains separately documented.

## New: installable Splunk SOC authentication lab

**Splunk dashboard proof now published:** [View the actual cropped Splunk screenshot](assets/evidence/splunk-native-dashboard-results.png), which shows the one-panel **Don Lopez — SOC Authentication Investigation** dashboard within Search & Reporting displaying five expected synthetic results. [Observation and evidence limits](splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md). Six-panel XML, indexed ingestion and alerts remain unverified. The screenshot is genuine application evidence; generated design illustrations are identified separately.

**If the custom Splunk application opens a 404**, use the [no-install native dashboard workaround](splunk_workflow/NO_APP_GUIDE.md). It starts in the working Search & Reporting UI and can be created by **Save As → Dashboard Panel**. A [standalone six-panel XML dashboard](splunk_workflow/NO_APP_DASHBOARD.xml) is also available to paste into a Classic dashboard, with no app installation, lookup, index or network calls.

The [Splunk workflow kit](splunk_workflow/README.md) now includes **two Six-panel Simple XML dashboards**, a matching 64-row CSV lookup, nine investigative SPL searches, and one **disabled** saved alert. The [CI-generated `.spl` application archive](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions) is available as the `don-lopez-splunk-soc-app` artifact in successful workflow runs.

The lookup-based dashboard can be inspected without creating an index. The indexed dashboard, true CSV ingestion, and alert firing still require your own authorized Splunk execution and are **not claimed as completed**. See [ingestion](splunk_workflow/INGESTION.md), [alerting](splunk_workflow/ALERTING.md), and [runtime status](splunk_workflow/VALIDATION_CHECKLIST.md).

## Start here
- [SOC Analyst evidence overview](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-evidence.html) — dedicated recruiter-ready index of four synthetic labs, each with a source-linked report and test references.
- [GitHub-readable SOC Analyst evidence guide](docs/SOC_ANALYST_EVIDENCE_GUIDE.md) — brief verified-versus-pending qualifications.
- [GitHub-readable project gallery](projects/CASE_STUDIES.md) — all six case studies without raw HTML or a 404.
- [Authentication detection case study](projects/authentication-detection.md) — reproducible, synthetic Python lab, 31 authentication tests, a simulated SOC investigation report, and a **seven-event Splunk smoke screenshot PASS; initial 64-event 3/5 boundary miss; corrected screenshot matches 5/5**.
- [Windows process execution triage case study](projects/windows-process-triage.md) — synthetic Windows Event ID 4688 exercise, 11 tests, ATT&CK hypotheses T1059.001 and T1105.
- [Network Traffic Analysis](projects/network-traffic-analysis.md) — PCAP generator, DNS/HTTP inspection, 18 tests, synthetic case report, and three [offline evidence images](assets/network/pcap-evidence-overview.svg).
- [Vulnerability Assessment & Remediation](projects/vulnerability-remediation.md) — localhost-only before/after HTTP hardening, 4 synthetic findings fixed, 16 tests.
- [Recruiter overview](docs/RECRUITER_OVERVIEW.md) — skills mapped to public evidence.
- [SOC analyst workflow](docs/SOC_TRIAGE_PLAYBOOK.md), [incident triage playbook](docs/SOC_TRIAGE_PLAYBOOK.md), and [analyst handoff template](docs/ANALYST_HANDOFF_TEMPLATE.md).
- [Detection evidence matrix](docs/DETECTION_EVIDENCE_MATRIX.md) and [résumé-ready project bullets](docs/RESUME_PORTFOLIO_BULLETS.md).
- [Celestial Resonance case study](projects/celestial-resonance.md) — responsible high-level summary of reproducible software research, quality gates, and auditability.
- [RAI case study](projects/research-ai-infrastructure.md) — high-level summary of evidence provenance, permission boundaries, and governed research tooling.
- [Future lab backlog](projects/PLANNED.md) — **planned**, not claimed as completed.

## Run all four security labs
Requires Python 3.10+; no dependencies or cloud resources.

```bash
python -m unittest discover -s projects/01-authentication-detection -p 'test_*.py' -v
python -m unittest discover -s projects/02-windows-process-triage -p 'test_*.py' -v
python projects/01-authentication-detection/detect_auth.py projects/01-authentication-detection/auth_events.csv
python projects/01-authentication-detection/validate_matrix.py
# The next step requires an authorized Splunk instance; see SPLUNK_RUNBOOK.md
python projects/02-windows-process-triage/process_triage.py projects/02-windows-process-triage/events_4688.csv
python projects/03-network-pcap/generate_fixture.py --output projects/03-network-pcap/synthetic_traffic.pcap
python projects/03-network-pcap/analyze_pcap.py projects/03-network-pcap/synthetic_traffic.pcap
python -m unittest discover -s projects/03-network-pcap -p 'test_*.py' -v
python projects/04-local-vulnerability-assessment/audit_demo.py
python -m unittest discover -s projects/04-local-vulnerability-assessment -p 'test_*.py' -v
```

Expected: **76 Python tests across four synthetic exercises** (31 authentication, 11 Windows process, 18 network, 16 local vulnerability assessment). The authentication fixture flags one login sequence for `alice` from `192.0.2.15`; the process-creation fixture returns two triage candidates. None is proof of real intrusion or production security efficacy.

## Offline website archive

The [bundler source](scripts/build_site_bundle.py) also supports creating the same archive manually with:

```bash
python scripts/build_site_bundle.py --output cybersecurity-portfolio-site.zip
```

Extract the ZIP fully before opening `index.html`. GitHub Actions generates a ready-made copy automatically on every successful `main` build.

## GitHub Pages hosting

Pages is configured for this repository. The static site uses small, dependency-free JavaScript modules for optional project filtering and interactive public teaching checks. Case studies, evidence links, and contact navigation remain available without JavaScript. It uses no framework, runtime credentials, analytics, external fonts or paid hosting. For hosting configuration, troubleshooting, and offline backup instructions, see [the site guide](docs/SITE_LAUNCH.md). [Check the latest Pages and website-health workflows](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions).

## Public disclosure and accuracy
- CR and RAI are **private** engineering projects. Do not publish their source, internal records, repository URLs, security-sensitive workflow details, or artifacts without a separate review.
- Case studies are based on high-level architecture and development methods, and **do not** establish a production security system, an independent penetration test, or quantified business/security gains.
- All four labs use synthetic events or localhost-only fixtures; no real systems are scanned and no real network packets are captured. Seven-event synthetic SPL smoke output matched an operator screenshot from Splunk; the first 64-event search returned 3/5 expected findings, while the corrected explicit-boundary screenshot matches 5/5. The query and job ID are not visible in the cropped result. Indexed-data qualification and production effectiveness remain unverified.
- Project status and evidence limitations are visible on each case-study page.
- CompTIA Security+ and CySA+ are listed based on the owner's report; no independent public verification or current-renewal status is asserted.

See [SECURITY.md](SECURITY.md) for disclosure handling and [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before future updates.

## Structure
```text
index.html, styles.css               Static website
projects/*.html                    Designed Pages case studies
projects/*.md                      GitHub-native readable versions of all six case studies
projects/01-authentication-detection/   Executable authentication lab
projects/02-windows-process-triage/     Executable Windows event triage lab
projects/03-network-pcap/              Generated PCAP exercise with source, tests, case report
projects/04-local-vulnerability-assessment/ Toy localhost web hardening + before/after audit
docs/RECRUITER_OVERVIEW.md            Skills mapped to evidence
projects/PLANNED.md                Honest roadmap
.github/workflows/validate.yml      Small focused CI checks + offline site preview archive
```

## License
No public reuse license is granted at this time. All rights reserved unless specified otherwise.
