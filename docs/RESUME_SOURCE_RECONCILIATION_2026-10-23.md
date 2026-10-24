# Résumé source reconciliation — October 23, 2026

**Public display name:** Don Lopez. The uploaded résumé was supplied privately to correct factual omissions in the website. Its full personal-name field, phone number, and source PDF **are not uploaded to the repository**.

## What the supplied résumé actually reports

| Area | Résumé-derived content | How this portfolio presents it |
| --- | --- | --- |
| Role focus | Cybersecurity Analyst / Security Operations | Pursuing SOC and Security Analyst roles; no paid SOC tenure implied |
| Location / public contact | Indio, California; existing approved email; public GitHub and LinkedIn profile links | Indio and previously approved email may appear; private phone omitted |
| Education | **B.S. Information Systems & Technology (Cybersecurity)**, California State University, San Bernardino | Exact program and university; graduation month December 2024 is owner-provided |
| Employment | **Allied Universal, Security Officer, 2019–present** | Clearly labeled professional experience, distinct from technical lab projects |
| Duties | Secure-environment monitoring, security logs, incident reports and escalation; source reports 10+ monthly reports | Qualitative responsibilities only; the quantitative volume is **not independently verified** |
| Certifications | Security+ certified; CySA+ earned October 2026 | Holder/résumé-reported until issuer-backed evidence is approved for publication |
| Planned qualification | Splunk Certified Cybersecurity Defense Analyst (SCCDA), **planned** | **Not earned**; planned preparation only |
| Skills | SPL, Sigma, Snort, MITRE ATT&CK, alert triage; Wireshark/Nessus/Nmap/Metasploit; Linux, Windows Server, VMware, Docker, basic AWS; Python, Bash, PowerShell, SQL | Distinguish current public-lab demonstrations from broader résumé-reported exposure |

## Important source-to-repository distinction

The supplied résumé **reports** several additional laboratory outcomes that cannot presently be reconciled to the four public fixtures:

- Five or more SPL/Sigma rules, including brute force, encoded PowerShell and lateral movement.
- A roughly 30% false-positive reduction during lab tuning.
- Splunk dashboards and alerts correlating three or more sources.
- A separate Kali/Wireshark/Snort lab analyzing more than 5,000 packets.

Those entries are **source-reported, not independently verified here**. They do not replace the repo-backed authentication, endpoint, network and localhost-hardening outcomes. Do not combine 5,000+ self-reported packets with the verified **20-frame synthetic PCAP**, or claim a 30% improvement for the fixed five-finding Splunk training case. If corresponding evidence is later supplied and checked, they may become independently inspectable projects.

## Existing publicly inspectable evidence

- **Authentication / Splunk:** 64 fabricated events, nine scenario families, original 3/5 expected findings corrected to 5/5 with inclusive 600-second logic; genuine cropped one-panel result.
- **Windows:** Five synthetic Event 4688 records, two review candidates and three nonmatching controls; 11 tests.
- **Network:** Generated 20-frame DNS/HTTP capture, 12 decoded observations, two review signals; 18 tests.
- **HTTP:** Four deliberately failing localhost response checks reduced to zero on the fixed fixture; 16 tests.
- Four labs total **76 focused Python tests**. None establishes real production monitoring or incident-response performance.

## Publication boundary

The public portfolio intentionally uses **Don Lopez**, not the complete identity shown on the supplied document. It does not publish the private phone number or original uploaded résumé PDF. The existing approved professional email is retained. Employment and credential information is visibly attributed to the owner's résumé, not described as third-party-verified. A private job submission can use appropriate legal/contact details after the owner reviews the final copy.

**This is a provenance and résumé-alignment record, not an employer reference check, issuer verification, or assertion that all source résumé claims have been independently reproduced.**


## October 24 public derivative

The primary public resume is now `resumes/Don_Lopez_Cybersecurity_Resume.pdf`.
It is derived from the privately supplied master by changing the display name to
Don Lopez and omitting the private phone. All remaining substantive text was
compared with the master and preserved. The private original remains unchanged
and outside this repository. Older role drafts are retained as legacy routes;
they are not the primary resume. The distinctions above between broader resume
lab work and the smaller public fixtures still apply.

## October 24 evidence follow-up

The public repository and the available file searches did not yield the original
artifacts for the larger resume labs. This is a retrieval limit, not evidence
that the original work was not done. Preserve the supplied resume and collect
the corresponding artifacts before claiming that the small public exercises
verify those projects.

| Resume project | Public evidence available now | Original material needed to connect the project |
| --- | --- | --- |
| Detection engineering: 5+ SPL/Sigma rules and roughly 30% fewer false positives | [Authentication query and boundary retest](../projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST_RESULT_2026-10-23.md); [Windows triage source](../projects/02-windows-process-triage) | The original SPL/Sigma rule files; representative input events; before/after false-positive counts with their denominator and tuning procedure |
| Splunk investigation using 3+ log sources | [Public synthetic Splunk workflow](../splunk_workflow/README.md), one genuine result-panel crop and reproducible training queries | Original source inventory, field mappings, query/dashboard exports and an investigation showing how those sources were correlated |
| Kali/Wireshark/Snort investigation of 5,000+ packets | [Generated 20-frame packet lab](../projects/03-network-pcap/CASE_REPORT.md) and its analyzer | Original shareable capture or trace, packet-count evidence, relevant Snort rules/alerts and analyst notes identifying the actual finding |

Each recovered artifact should retain its date, tool/version context and data
origin, with sensitive fields removed where appropriate. The 20-frame fixture
must not be relabeled as the larger capture, and the 5-of-5 synthetic finding
result must not be presented as the resume's false-positive reduction.
