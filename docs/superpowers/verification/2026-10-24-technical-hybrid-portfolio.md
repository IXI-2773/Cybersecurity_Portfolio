# Technical portfolio verification receipt

Implementation candidate: `74ddc2270f44ede3f20dabe9d31f847e8f231daf`.
PR: https://github.com/IXI-2773/Cybersecurity_Portfolio/pull/12

## Result

- GitHub Validate public portfolio: success, run `40112213195`.
- GitHub Review responsive website in Chrome: success, run `40112213189`.
- Local pure behavior checks: 19 authentication/replay, 21 vintage/claim, 17 legacy API compatibility; 3 technical-fixture Python tests.
- Both generated fixture freshness checks passed. Static links, evidence consistency, core accessibility structure, and genuine Splunk PNG integrity passed.
- Chrome exercised four target routes at 1280, 390, and 320 pixels; image loading, no JavaScript errors, and no document overflow. Keyboard selection retained focus in all three inspectors. Earlier successful-login selection, below-threshold results, CR ambiguity, RAI scope/attribution, reduced motion, hidden/offscreen pause, and no-JavaScript fallbacks passed.
- The existing wider portfolio navigation, screenshots, résumé preservation, and mobile-menu checks also passed.

## Review corrections

The independent source review identified lost keyboard focus after selection, an inspector bound to the last rather than selected successful login, and an ambiguity example with inherited rather than accurate provenance. Focus restoration, selected-decision binding, and a canonical hashed ambiguity fixture correct those issues. Added regressions for selected success/account binding and ambiguity-record hashes failed before correction and passed afterward. Real Chrome tests verify the focus behavior.

Also added the inline Python source excerpt, source-event selection in Signal to Case, and selectable passage-to-claim relationships. The browser count display explicitly describes counts rather than implying a runtime identity comparison; independent fixture tests compare complete finding identities. Unenhanced stage buttons remain hidden without JavaScript.

## Decisions and limits

- Use native implementation and one bounded source review, as specified in the approved plan.
- Add a canonical public research JSON file and a generator so record hashes and fixture identity can be reproduced.
- Use the existing GitHub Chrome CI workflow for rendered verification: local Chrome cannot create a process socket, and the cloud browser blocks file URLs. No workaround to that browser restriction was used.
- Replace obsolete diagram-specific browser checks with current workbench checks while retaining the wider no-JavaScript/navigation/image review.
- The design review does not validate private CR/RAI source, forecasting performance, résumé metrics, or unpublished original labs. Existing source qualifications remain visible.
- Real image assets and campus gallery are preserved. No original VM/Wireshark/E3/HackThisSite screenshot was fabricated or newly recovered.
- No merge or production deployment is included in this receipt.
