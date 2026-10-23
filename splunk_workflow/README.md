# Splunk End-to-End SOC Authentication Lab

**Owner:** Don Lopez · **Source:** 64 synthetic authentication rows, nine scenarios, five expected correlation matches.

**Status:** Application/dashboard/alert package **PREPARED — installation, true CSV ingestion, dashboard rendering, and alert triggering are NOT YET VERIFIED in your Splunk Enterprise trial.** The separate original seven-event smoke search passed and the corrected 64-row in-memory SPL returned a screenshot with five expected rows; those do not validate this packaged app or indexed behavior.

## What is ready to use

| Component | Artifact | Deployment state |
| --- | --- | --- |
| Self-contained demo | [Splunk app source](../splunk_app/don_lopez_soc/) + lookup `portfolio_auth_validation.csv` | Prepared; independent of index and ingest |
| SOC dashboard — demo | `auth_triage_demo` Simple XML page | Not run in your instance |
| SOC dashboard — indexed | `auth_triage_indexed` Simple XML page | Requires actual authorized CSV ingestion |
| Nine focused searches | [SPL search files](searches/) | Not yet run as this package |
| Saved alert | Disabled `Portfolio SOC Auth Candidate - Indexed (DISABLED)` | Disabled; no automatic action |
| Installation package | CI build artifact `don-lopez-splunk-soc-app` / generated `.spl` file | Source/build verification only |

## Fastest path: deploy the demo dashboard without an index

1. In [GitHub Actions](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions), open a **successful Validate public portfolio** run. Under Artifacts download `don-lopez-splunk-soc-app` and extract its ZIP wrapper.
2. Find the `don_lopez_soc.spl` file. In Splunk Enterprise as an authorized administrator, open **Apps → Manage Apps → Install app from file**, select the `.spl` archive, and follow any restart instructions. Review the package source first; it contains only CSV, dashboard XML, and a **disabled** saved search. Do not upload secrets.
3. Open **Don Lopez | SOC Authentication Lab** → **SOC Authentication | Bundled Synthetic Demo**. This reads the app's lookup with `inputlookup`, not indexed events.
4. Expected: 64 events, nine scenario labels, two counts/charts/tables, and five candidate detections under the inclusive 600-second rule. Take actual Splunk screenshots **only after viewing these results**.
5. If the dashboard shows a missing lookup warning, verify installation and app context. Do not claim a successful dashboard until observed.

## Next: genuine CSV indexing and investigation

Follow [the ingestion guide](INGESTION.md), which uses the original fixture in a **separate isolated test index** with CSV field extraction, UTC timestamp verification, no duplicates, and explicit checks. The indexed dashboard will remain empty until ingestion works.

## Controlled alert demonstration

Follow [the alert runbook](ALERTING.md). The bundled alert is *disabled* and does not email, send webhooks, run scripts, or isolate hosts. The alert preview can be tested manually; **historical 2026-10-05 data will not trigger a live last-five-minutes alert on today's date**. Creating a controlled alert with current fabricated events is a separate authorized operation and has not been performed.

## Limits

- No real identity provider, user credentials, or operational telemetry.
- The bounded demonstration detector uses `streamstats list()` and explicit inclusive time arithmetic; Splunk's multivalue list cap makes it **unsuitable as a general high-volume production correlation rule** without redesign.
- Dashboard XML is syntactically checked in CI but still requires actual Splunk renderer/runtime verification.
- Neither a passing code test nor installation alone establishes an actual incident, live alert, or production effectiveness.

See [verification checklist](VALIDATION_CHECKLIST.md).
