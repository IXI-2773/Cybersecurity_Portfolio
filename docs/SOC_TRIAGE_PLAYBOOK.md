# SOC Analyst Triage Playbook — Synthetic Portfolio Cases

**Owner:** Don Lopez  
**Scope:** Fabricated authentication and Windows process-creation exercises  
**Authorization:** Read-only analysis. This document grants no permissions to scan, access hosts, disable accounts, execute malware, or modify any system.

## Objective

A detector match is a **lead**, not confirmation of compromise. Establish what occurred, test plausible explanations, and prepare an evidence-backed handoff under an organization's authorized procedures.

## Analyst workflow

| Step | Question | Evidence expected | Stop / review condition |
| --- | --- | --- | --- |
| Intake | What rule, log source, time and asset produced this alert? | Unique case ID, original log reference and time range | Provenance missing → hold |
| Verify | Do the real event values actually satisfy the rule? | Recomputed predicate, normalization and timestamp integrity | Invalid fields or uncertain ordering → hold |
| Scope | Which users, hosts and network sources are relevant? | Bounded impact candidates and authorized investigation scope | Unknown asset ownership → do not assume access |
| Corroborate | Is there independent supporting or contradictory telemetry? | Identity, endpoint and network citations with source IDs | Single heuristic alone → do not claim compromise |
| Assess | What benign explanations and impacts remain plausible? | Confidence, explicit gaps, provisional severity | Unknown impact → label as unknown |
| Disposition | Is escalation, further review or closure justified? | Reasoned disposition and next authorized action | No unilateral containment without authority |
| Handoff | Can a second analyst reproduce the reasoning? | Timeline, source references, exact queries, owner | Evidence incomplete → request follow-up |

## Case A: Authentication burst — LAB-AUTH-001

The fabricated data has six failed logins followed by a successful login for `alice` from documentation IP `192.0.2.15`. The rule groups by account and IP and resets the failure streak after **every** success. The behavior is **consistent with** a [T1110 brute force](https://attack.mitre.org/techniques/T1110/) hypothesis but also compatible with legitimate mistakes.

**Missing:** MFA activity, actual user/device history, session actions, credential changes, endpoint findings. **Disposition:** synthetic triage signal; no real intrusion determined. [Read the case report](../projects/01-authentication-detection/SOC_CASE_REPORT.md).

## Case B: Windows process execution — LAB-PROC-001

Two fabricated Windows Event 4688 records flag encoded-command PowerShell and certutil URL-cache flags. These are investigation hypotheses aligned to [T1059.001](https://attack.mitre.org/techniques/T1059/001/) and [T1105](https://attack.mitre.org/techniques/T1105/); benign administration is a credible alternative.

**Missing:** executable signature, process lineage beyond the fixture row, script content, payload hash, proxy logs, approved admin context. **Disposition:** candidate findings for analyst review; no malicious execution confirmed. [Read the Windows case study](../projects/windows-process-triage.html).

## Provisional severity bands — illustrative, not an employer's policy

| Band | Evidence posture | Possible recommendation |
| --- | --- | --- |
| Informational | Benign explanation supported by reviewed sources | Document and close or monitor |
| Needs review | Detector matched; additional data unavailable | Request scoped corroboration |
| Elevated | Independent supporting evidence and credible affected asset | Escalate to owning team |
| Critical | Strong evidence of severe impact and response criteria met | Notify authorized incident command; no self-directed containment |

## Evidence and safety

Preserve raw data references, source provenance, UTC normalization, rule version and negative observations. Store live evidence only in an authorized organization system, not this public portfolio. The [handoff template](ANALYST_HANDOFF_TEMPLATE.md) and [coverage matrix](DETECTION_EVIDENCE_MATRIX.md) preserve the separation between facts, hypotheses and missing information.

These are **methodology artifacts**, not evidence of live SOC employment, completed investigations of actual incidents, or independently validated enterprise detections.
