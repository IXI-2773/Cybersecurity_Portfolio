# Splunk SOC Lab — Execution and Verification Runbook

**Owner:** Don Lopez · **Data:** synthetic only · **Status:** offline Python scenarios checked; Splunk runtime execution **NOT YET VERIFIED**.

## Objective
Detect >=5 failed logins within a rolling 10-minute window for the same user and source IP, followed by a success. Any success clears that key's previous failures, **including a non-alerting success**. A detection signals analyst review, not a real compromise.

## Prerequisites
- Access to a Splunk Enterprise / Cloud search environment where you are authorized to upload synthetic CSV data.
- Permission to use a dedicated test index such as `lab_auth`; otherwise replace `index=lab_auth` in the SPL with your permitted index.
- An upload mechanism that extracts CSV headers as fields; assign sourcetype `portfolio:auth` or replace it consistently in the query.
- **No credentials or real organization data** in these fixtures.

## 1. Upload and verify
1. Open Splunk's **Add Data → Upload** (interface labels vary by version).
2. Upload [`validation_events.csv`](validation_events.csv), choose CSV source type / field extraction, map the `timestamp` field, UTC format `%Y-%m-%dT%H:%M:%SZ`, and select the permitted destination index. Check that time extraction is correct before submitting.
3. Check that the **event-time** range includes **October 5, 2026**, and use the corresponding time picker range (or All time for the isolated test index).
4. Run:
   ```spl
   index=lab_auth sourcetype="portfolio:auth"
   | stats count as events dc(username) as distinct_users by source
   ```
5. Inspect at least two raw events and confirm extracted fields: `timestamp, username, source_ip, host, event_type, scenario`. A wrong time picker or field extraction is an ingestion issue, not a detection result.
6. If you previously uploaded a fixture, use a fresh lab index or carefully filter `source` to avoid duplicate ingestion. **Do not erase production data.**

## 2. Run the detection search
Paste [`splunk.spl`](splunk.spl) into Splunk Search, replacing the index/sourcetype selectors only if needed.

**Implementation detail:** The first `streamstats current=f` computes the number of *prior* successful logins per (username, source_ip), providing a streak identifier. After every success, the next event for that key belongs to a new streak. The second `streamstats time_window=10m` counts only failures in the current streak. Sorting by global `_time` ensures that the time window is forward-looking in event processing order. Events with equal timestamps need an explicit deterministic tie-breaker; this fixture avoids ties.

The query is **SPL (Splunk Search Processing Language)**, not SPL2. Splunk's `streamstats` has a configurable maximum event window (often 10,000 events), so large-scale ingestion needs separate qualification.

## 3. Compare results against an independent expected fixture
Export the **Statistics** search results as CSV, e.g. `splunk_results.csv`, ensuring the fields `timestamp, username, source_ip, failure_count_in_window` are present.

Run:
```sh
python projects/01-authentication-detection/validate_matrix.py
python projects/01-authentication-detection/validate_matrix.py --splunk-export path/to/splunk_results.csv
```

The first command checks the **Python reference detector** against the fixed expected matrix; it **does not execute Splunk**. The second compares whatever CSV the user supplied to the independent expected fixture; passing alone does not establish who generated that CSV.

Expected: **5 findings** (and 4 non-detecting scenario families) across these nine synthetic scenarios:

| Scenario | Expected alerts | Reason |
| --- | ---: | --- |
| threshold | 1 | five failures, then success |
| below | 0 | only four failures |
| intervening_success | 0 | earlier benign success breaks the streak |
| post_success_burst | 1 | five *new* failures after benign success |
| expired | 0 | successes outside ten-minute window |
| other_user | 0 | failures cannot be borrowed from another account |
| other_ip | 0 | failures cannot be borrowed from another source IP |
| ten_minute_boundary | 1 | event exactly ten minutes prior is inclusive |
| interleaved_users | 2 | two independent username/IP sequences |

The expected JSON contains the **five exact timestamp/user/IP/count rows** and is independent of the implementation.

## 4. Capture employer-grade evidence (once actually executed)
- Screenshot of Splunk Add Data field/timestamp preview, with personal identifiers removed.
- Screenshot of query and the five result rows, with time picker and search index visible but no credentials.
- Saved Results CSV and its SHA-256 checksum.
- Actual Splunk product/version, index/sourcetype chosen, UTC/timezone settings, and any deviations from the runbook.
- A short paragraph explaining observed differences and how you resolved them.
- Verification output and local Python version, including any failing negative cases.

**Do not publish simulated Splunk screenshots or label Python output as live Splunk execution.**

## 5. Security and interpretation limitations
A five-failure success sequence is **not proof** of account takeover or password guessing; it can arise from authorized work. Conversely, source-IP rotation, missing events, NAT, clock skew, and distributed attempts can hide a real issue. Confirm MFA/identity logs, session behavior, account owner context and endpoint/network corroboration before asserting an incident.

## Sources
- [Splunk `streamstats` reference](https://help.splunk.com/en/splunk-enterprise/spl-search-reference/10.2/search-commands/streamstats)
- [Splunk source types and structured CSV extraction](https://help.splunk.com/en/splunk-cloud-platform/get-data-in/get-started-with-getting-data-in/10.2.2510/configure-source-types/manage-source-types)
- [Splunk timestamp parsing and UTC considerations](https://help.splunk.com/en/splunk-enterprise/search/search-manual/10.4/specify-time-ranges/how-time-zones-are-processed-by-the-splunk-platform)
