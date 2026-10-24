# Identity & MFA Investigation

A planned identity case that follows a suspicious sign-in through account and session context.

Sign-in logs · MFA · Account audit events

A scoped project brief with a clear investigation question and deliverables.

Planned project · Not yet executed

## The scenario

A training account shows repeated authentication attempts followed by a successful sign-in. The proposed case asks whether account changes, MFA events and session activity strengthen or weaken the initial compromise hypothesis.

## The investigation plan

- Build synthetic sign-in, MFA and account-change records with explicit timestamps.
- Correlate by stable account and session identifiers.
- Compare an attack-like sequence with legitimate retries and administrative activity.
- Document a provisional decision and the evidence an authorized response team would need.

## What I intend to publish

The fixture, event timeline, correlation queries, negative cases and an analyst handoff. The exercise will distinguish an authentication signal from a confirmed account takeover.

## Scope and evidence

This is a proposed project brief. There are no completed investigation results, screenshots or performance claims yet. They will be added after the work is performed.

Research reference

[MITRE ATT&CK: brute-force context ↗](https://attack.mitre.org/techniques/T1110/)

[Choose another case study ↗](../explore.html)
