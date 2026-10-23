# Hiring experience and verification workbench

User direction: add useful capabilities, improve hiring-team usability, expand CR/RAI and test engines. Continue in existing PR; preserve private-project boundaries and supported claims.

Implementation:
- Add explore.html: all six case studies plus workbench, role selection and keyword filtering, shareable initial role links, all content visible without JavaScript.
- Add test-lab.html: two local browser engines (authentication replay and attributed-evidence coverage), executable checks with real computed results, adjustable auth window, readable observations and downloadable run receipt. Explain that the public engines are separate from private CR/RAI and the Python suite.
- Generate browser fixture data from the existing public CSV and frozen expected JSON; retain source hashes and fail checks on stale data.
- Expand CR and RAI with clear architecture, test strategy and links to public counterparts. Give hiring teams a concise homepage starting path.
- Keep the static architecture. No backend, account, model API, analytics, added dependencies or uploaded visitor input. Use native form controls and textContent for dynamic output.
- Check engine boundary/negative/error behavior, exact frozen-matrix parity and fixture freshness. Exercise explorer empty/reset/combined filtering and workbench success/hold/error states in the existing browser workflow. Reuse existing semantic/link/evidence audits and website archive helper.

Public engines are independently authored demonstrations. They do not claim to run private CR/RAI code, perform semantic truth verification, or establish production detection performance.

Implemented: project explorer, two independent public engines, generated fixture with source hashes, browser receipt export, hiring start routes, expanded CR/RAI testing sections, all-site navigation, and offline bundle support. Focused checks pass: 14-page semantic audit, 363 local links, frozen evidence consistency, fixture freshness, nine baseline engine checks plus invalid/duplicate/unsupported source controls. Browser workflow expanded to cover filtering, no-JS explorer, 599/600 replay, coverage verdicts and actual receipt download. Final CI at head `71ea95d6397cc2b8f9e2c4c7da3af987f2341201`: [source validation passed](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions/runs/39993194253) and [real Chrome responsive review passed](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions/runs/39993194251). Chrome exercised the filter/no-JavaScript path, baseline checks, 599/600-second replay, coverage holds, receipt download, and page overflow. A later documentation-only commit does not change the tested scripts, fixtures, styles, or HTML.
