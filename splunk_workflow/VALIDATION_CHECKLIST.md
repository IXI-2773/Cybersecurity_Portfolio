# Splunk Evidence Admission Checklist

Only change status based on genuine Splunk screenshots, exports or verified job metadata.

| Milestone | Prepared artifacts | Execution evidence | Allowed claim |
| --- | --- | --- | --- |
| Previous 7-event SPL smoke | Query | Screenshot-reviewed 1/1 | Small synthetic SPL smoke passed |
| Previous 64-event SPL matrix | Query and five-row oracle | Initial screenshot 3/5; cropped corrected results 5/5 | Bounded screenshot consistency; job provenance unverified |
| Bundled CSV lookup dashboard | Splunk app, CSV, Simple XML | **Not yet executed** | App source prepared; not demo runtime success |
| Indexed CSV investigation | Upload guide, dashboard and SPL | **Not yet executed** | Prepared only |
| Alert configuration | Disabled saved search, preview, guide | **Not yet executed** | Disabled definition prepared only |
| Actual scheduled trigger / throttle | Guide | **Not yet executed** | No trigger claim |

**Release rules:** Never fabricate screenshots, real incident timelines, job identifiers, triggered alert logs or ingestion results. Treat browser-rendered portfolio charts as presentation, not proof Splunk ran.

## Operational completion criteria (optional)

- Lookup demonstration: 64 records, nine scenarios, five findings visible in a real Splunk dashboard.
- Indexed data: 64 raw events, correct fields/UTC times, five original oracle findings from indexed search, documented index and source metadata.
- Alert: harmless synthetic-only trigger, specified schedule, observable triggered-alert event, suppression behavior and no unauthorized external actions.

## Native fallback — 404 bypass

[No-App Dashboard Guide](NO_APP_GUIDE.md) and [single-source Classic XML](NO_APP_DASHBOARD.xml) are prepared as the preferred alternative to installing a custom Splunk application. They require no index, lookup or package upgrade. The prior corrected query's five-row Statistics screenshot is already reviewed; **no independently observed dashboard rendering** has been supplied yet.

## App navigation regression — observed 404

A Splunk Enterprise 404 image was provided after the first v1.0.0 package, but the URL was not visible. The **1.0.1** package removes unresolved navigation targets, adds app/view/lookup metadata, and increments the build. A new **actual in-product dashboard screenshot** is still required to close this as a verified repair. See [404 diagnostics](README.md#resolving-a-splunk-404-after-installation).
