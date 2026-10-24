# Python SOC Triage Assistant

A planned local tool for turning exported security events into a reviewable case summary.

Python · CSV/JSON · Schema validation · Reporting

A scoped project brief with a clear investigation question and deliverables.

Planned project · Not yet executed

## The problem

Exported logs can have inconsistent field names, missing timestamps and duplicate events. A small triage utility could organize those inputs while keeping the original rows available for analyst review.

## The build plan

- Accept local CSV and JSON fixtures and validate required fields.
- Normalize timestamps and identifiers while preserving source-row references.
- Group related observations and flag incomplete or ambiguous records.
- Produce a readable summary that links every finding back to the input.

## What I intend to publish

A command-line utility, synthetic input files, deterministic output, malformed-input tests and a sample report. It will organize evidence, not autonomously contain hosts or declare incidents confirmed.

## Scope and evidence

This is a proposed project brief. There are no completed investigation results, screenshots or performance claims yet. They will be added after the work is performed.

Research reference

[Splunk source-correlation background ↗](https://help.splunk.com/en/splunk-enterprise-security-8/administer/8.5/detections/use-detections-to-search-for-threats-in-splunk-enterprise-security)

[Choose another case study ↗](../explore.html)
