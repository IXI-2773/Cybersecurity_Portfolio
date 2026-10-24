# Multi-source Splunk Investigation

Connect authentication, endpoint and network activity into a readable investigation.

Splunk · Log correlation · Incident timelines · 2025

Résumé lab: dashboards, alert triage and correlation across 3+ log sources.

## The investigation problem

An authentication alert answers only part of an incident question. Understanding what happened requires connecting the account activity to relevant endpoint and network observations, while keeping the sequence and source of each event clear.

## My lab work

My résumé describes building Splunk dashboards and alerts for authentication anomalies and rapid login attempts. I correlated authentication, network and endpoint logs across three or more sources, constructed event timelines and documented investigations.

I also optimized SPL queries to reduce false positives. This case describes that broader lab work; original dashboard exports and multi-source event samples are being organized for publication.

## The investigation structure

**Identity context**
Review the account, source address, failure/success sequence and relevant authentication time range.

**Endpoint context**
Look for related execution on the affected system and distinguish suspicious commands from expected administration.

**Network context**
Correlate relevant destinations and connection timing without treating every unusual request as malicious.

**Case timeline**
Keep each event attached to its source, explain gaps and end with a reasoned disposition.

## A decision, not just a dashboard

The report should explain whether the reviewed evidence supports escalation, further collection or a benign explanation. A populated dashboard alone cannot make that decision; an analyst needs to explain the relationships and remaining uncertainty.

## Public work available now

The independent Splunk authentication case contains the published training fixture, corrected query and observed dashboard panel. The analyst workflow shows how I structure validation, corroboration and handoff.

[Inspect the public Splunk case ↗](authentication-detection.md) · [Read my analyst workflow ↗](soc-analyst-workflow.html)

## Scope and evidence

Completed lab work described in my supplied résumé. The original lab artifacts and screenshots will be added here; the linked public exercises have their own, smaller scope. This is lab experience, not a claim of a production incident or paid SOC employment.

Background reference

[Splunk documentation: detections and source correlation ↗](https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.5/detections/use-detections-to-search-for-threats-in-splunk-enterprise-security). This reference informs the investigation approach; it does not verify my lab results.

[Choose another case study ↗](../explore.html)

## Academic foundation

Completed coursework: IST 5250 Incident Handling & Cyber Investigation (Fall 2024), alongside database management and big data analytics coursework.

[Explore the academic background](../education.html).
