# Simulated SOC investigation — failed-logon burst followed by success

**Prepared by:** Don Lopez  
**Case:** LAB-AUTH-001 · **Classification:** Synthetic defensive exercise, **not a real security incident**  
**Evidence source:** [`auth_events.csv`](auth_events.csv) (hand-crafted 16 records)  
**Analysis implementation:** [`detect_auth.py`](detect_auth.py) · **Splunk status:** search drafted; no verified Splunk run

## Investigation prompt
Is the successful login at **2026-10-01 09:06 UTC** for fabricated account `alice` from reserved address `192.0.2.15` preceded by enough failed attempts to justify investigating a possible brute-force sequence?

## Reconstructed event timeline (fabricated)
| Time UTC | Event | Analyst observation |
| --- | --- | --- |
| 09:00–09:05 | Six login failures | Same account and same source IP within 5 minutes |
| 09:06 | Login success | Same account/IP immediately after the failures |
| 09:07–09:09 | Two failures then success for `bob` | Does not meet five-failure threshold |
| 09:10–09:14 | Five failures for `charlie` | No matching success appears |
| 09:15 | Login success for `alice` from another IP | Does not inherit prior source-IP history |

## Observable facts vs hypotheses
**Verified within the fabricated CSV:** The Python reference flags exactly one sequence: `alice` / `192.0.2.15`, 6 failures, success at 09:06 UTC. The date, address, accounts and events are invented. The original fixture is not proof of adversarial activity.

**Hypothesis to investigate in a real environment:** Password guessing followed by valid authentication is consistent with [MITRE ATT&CK T1110](https://attack.mitre.org/techniques/T1110/); alternate explanations include an authorized user mistyping a password or administrative automation.

**Evidence not available:** MFA challenges, session tokens, device posture, geolocation and reputation context, privileged operations, subsequent endpoint behavior, historical baselines, or an identity-provider audit trail.

## Analyst decision
**Disposition:** `SIMULATED_TRIAGE_SIGNAL — NO REAL INCIDENT DETERMINED`.

In a real authorized SOC workflow, review supporting authentication logs, MFA and session telemetry, device activity, recent credential changes and legitimate access context. Escalate only if evidence corroborates account compromise. Do not recommend disabling an account solely from this synthetic threshold match.

## Detection quality review
The original detector had a meaningful logic issue: sub-threshold successes did not clear the failed-login queue, allowing failures from an earlier streak to be carried into a later success. The updated Python reference clears the queue **after every success**, and the revised SPL design divides the stream into separate login streaks. Nine synthetic validation scenario families explicitly cover the corrected behavior, boundary cases and other identities.

**Verification limit:** Python unit tests and the validation corpus can establish internal fixture behavior, but do not demonstrate real-world accuracy, performance, operational security impact, or runtime equivalence with Splunk. Follow [`SPLUNK_RUNBOOK.md`](SPLUNK_RUNBOOK.md) for the separate Splunk execution and artifact capture steps.
