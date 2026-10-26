# Application Readiness — Don Lopez

This guide accompanies the public [application toolkit](https://ixi-2773.github.io/Cybersecurity_Portfolio/apply.html) and the two plain-text résumé drafts. The résumé files are starting materials to tailor truthfully, **not claims of prior paid SOC employment**.

## Select a role-specific version

| Target | Copy/download | Best first interview example |
| --- | --- | --- |
| SOC Analyst / Tier 1 SOC | [SOC Analyst ATS text](../resumes/Don_Lopez_SOC_Analyst.txt) | Recorded AD host/packet correlation, then Splunk 3/5 → 5/5 boundary debugging |
| Cybersecurity / Security Analyst | [Security Analyst ATS text](../resumes/Don_Lopez_Security_Analyst.txt) | Local HTTP hardening from four fixture-rule hits to zero; then recorded AD evidence correlation |

**Source anchors:** [Recorded AD investigation](../projects/ad-attack-chain.html) · [AD report](../projects/08-ad-investigation/CASE_REPORT.md) · [Genuine cropped Splunk screenshot](../assets/evidence/splunk-native-dashboard-results.png) · [Auth case](../projects/authentication-detection.html) · [Process case](../projects/windows-process-triage.html) · [Network case](../projects/network-traffic-analysis.html) · [Web remediation case](../projects/vulnerability-remediation.html).

## Current readiness record

| Application element | Status | Public handling |
| --- | --- | --- |
| Portfolio and case studies | **Ready** | Public GitHub website, recorded OTRF AD analysis, genuine cropped Splunk screenshot and controlled security labs |
| Two role-specific résumé drafts | **Ready to tailor** | Public text files include the approved professional email; owner-résumé-reported Security Officer experience; no invented employers or phone details |
| Professional profile | **Public** | [GitHub profile](https://github.com/IXI-2773); not represented as a guaranteed direct messaging channel |
| Professional email | **Publicly approved** | [frailtycraven@gmail.com](mailto:frailtycraven@gmail.com) appears on the website and both résumé drafts |
| Phone / other email addresses | **Not approved for public site** | Keep private unless separately authorized |
| Employment chronology | **Résumé-reported; not independently verified** | Allied Universal Security Officer, 2019–present. Physical-security work is separate from public technical labs and is not SOC employment |
| Security+ / CySA+ | **Holder-reported** | The supplied résumé reports CySA+ earned October 2026. Issue/expiry details for Security+ and issuer verification URLs remain unavailable; see [credential guidance](CREDENTIALS.md) |
| Production SOC experience | **Not established** | No invented employment, real incident investigation or live SIEM deployments |

[See publication gates](PUBLICATION_GATES.md) for the release record. **frailtycraven@gmail.com** is the approved direct contact; GitHub remains an evidence and professional-profile reference.

## Five-minute tailoring workflow

1. Read the job posting and highlight no more than five **required** capabilities; check each against code or a genuinely completed task. Do not add a tool you have merely heard of or a credential not held.
2. Choose the nearest résumé track and keep the text-only section headings **Professional Summary**, **Technical Skills**, **Selected Cybersecurity Projects**, **Education**, **Certifications**. Review the Allied Universal role and dates against employment records before submission; never invent experience.
3. Reorder two or three project bullets to match the posting. For a SOC job, foreground recorded AD evidence correlation, Splunk and investigative judgement; for a security analyst role, foreground HTTP response controls, repeatable remediation checks and host/network analysis.
4. Confirm **frailtycraven@gmail.com** remains the preferred email for employers. It appears in the public drafts. Add a phone number or alternative address only to a private copy unless separately authorized; review badge visibility and issued-to names before posting verification URLs.
5. Paste the plain text into your preferred résumé editor; proofread dates, links, line wrapping and final PDF before submitting. A text copy is provided for ease of ATS parsing, **not a guarantee of ATS performance or hiring success**.

## Interview verification map

- **Walk through a multi-source investigation:** start with the [recorded AD case](../projects/ad-attack-chain.html). Explain same-host process GUID/session joins, packet corroboration, the 39.812-second collection delay, alternative administration explanations and why six findings are not six confirmed compromises. Python analysis is reproducible; AD SPL/Sigma translations remain unexecuted candidates.

- **Walk through a Splunk investigation:** explain the original 3/5 result, why 600-second inclusivity matters, the revised SPL and the real native 5/5 screenshot. [Original discrepancy](../projects/01-authentication-detection/SPLUNK_MATRIX_FIRST_RUN_2026-10-23.md) · [Corrected query](../projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST.spl).
- **How do you differentiate signal from incident?** A rule hit is a lead; corroborate MFA, device, identity and session logs. The authentication fixture is synthetic; the AD investigation separately analyzes OTRF’s recorded emulation telemetry.
- **How do you test a fix?** Compare frozen expected findings before and after while preserving negative cases and scope. HTTP lab demonstrates four fixture-rule hits dropping to zero, not production security.
- **How do you handle missing telemetry?** State limitations and alternative explanations, do not invent supporting data. [Analyst handoff template](ANALYST_HANDOFF_TEMPLATE.md).

## Claims deliberately excluded

- No paid SOC analyst tenure was supplied. The separately identified Allied Universal Security Officer role is résumé-reported, not independently employer-verified.
- No real breach, attacker attribution, production Splunk alert, indexed ingestion, Wireshark screenshot, independently audited credential status, or enterprise remediation was established.
- No unverifiable precision/recall, detection latency, avoided losses, or threat statistics.

**Production incident-response and indexed Splunk deployment evidence are not established.**

**Document purpose:** evidence-backed job-application preparation, not credential endorsement or employment verification.
