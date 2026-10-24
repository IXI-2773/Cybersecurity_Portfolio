# Detection Engineering & Rule Development

Build detections that explain the behavior they match—and the benign activity they can confuse.

Splunk SPL · Sigma · MITRE ATT&CK · 2026

Résumé-reported lab outcome: 5+ detection rules and approximately 30% fewer false positives during validation.

## The investigation problem

A rule that matches a suspicious command or a login burst is a starting point. Its value depends on the behavior it is intended to detect, the data it needs and the legitimate activity that can produce the same pattern.

## My lab work

My résumé describes developing and testing more than five SPL and Sigma rules for brute-force activity, Base64-encoded PowerShell and lateral movement. I simulated attack scenarios, mapped the detections to ATT&CK and documented their logic.

The tuning work focused on reducing false positives during lab validation. The approximately 30% reduction is the result reported in my résumé; the original before-and-after event sets will accompany the detailed evidence when organized.

## How I explain a detection

- **Define the behavior.** State the account, host, command or time-window relationship that makes an event relevant.
- **Choose the telemetry.** Identify fields, timestamp meaning and required source coverage before interpreting a match.
- **Challenge the rule.** Compare simulated attack activity with benign administration and normal authentication failures.
- **Tune and document.** Record what changed, what was excluded and which blind spots remain.

## A public example you can inspect now

The separate authentication exercise preserves a missed boundary case, the corrected SPL and a genuine cropped Splunk result panel. The Windows exercise adds encoded PowerShell and certutil-style review candidates. These are smaller public examples, not the original five-rule collection.

[Inspect the Splunk boundary case ↗](authentication-detection.md) · [Review Windows command triage ↗](windows-process-triage.md)

## What the evidence will include

The original SPL/Sigma files, scenario inputs, rule explanations, ATT&CK mappings and the false-positive comparison. Those artifacts will make the broader lab work easier to reproduce and discuss.

## Scope and evidence

Completed lab work described in my supplied résumé. The original lab artifacts and screenshots will be added here; the linked public exercises have their own, smaller scope. This is lab experience, not a claim of a production incident or paid SOC employment.

Background reference

[MITRE ATT&CK: brute-force behavior ↗](https://attack.mitre.org/techniques/T1110/). This reference informs the investigation approach; it does not verify my lab results.

[Choose another case study ↗](../explore.html)
