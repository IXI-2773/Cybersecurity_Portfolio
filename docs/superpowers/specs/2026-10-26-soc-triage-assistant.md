# Exported-log SOC Triage Assistant

Implement the already-approved local CSV/JSON tool here, with no home-PC or live
Splunk dependency. One command produces JSON and a readable HTML handoff with a
UTC timeline, source-record references, duplicate accounting and quarantine.

Support declared authentication/process exports and explicit field aliases.
Require timezone-aware timestamps. Deduplicate declared stable event IDs only;
quarantine conflicting IDs. Preserve rows without IDs rather than silently
coalescing lookalikes. Detect a bounded failure-to-success sequence and reuse the
existing process-pattern inspector. Findings remain analyst review candidates.

Retain real executed demo output, input/source hashes and a reproducible check.
Replace the planned case with the completed tool and an actual-output walkthrough.
Link it under tools, run focused tests and existing CI, review, and auto-merge.
Do not collect endpoint data, run input commands, connect services or contain hosts.
