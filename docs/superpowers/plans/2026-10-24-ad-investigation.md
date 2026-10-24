# Public Active Directory capture investigation

Owner approved the source-intake proposal and requested the complete correlated investigation, detections, and alternative explanations. Continue the existing static portfolio and hybrid inspector pattern; publish only supported findings.

## Task 1 — Evidence and tested analysis

- [ ] Build a standard-library Python analyzer/downloader in `projects/08-ad-investigation/analyze.py`. Accept only the pinned two ZIP archives from the intake manifest, hash-check before parsing; never extract/run payloads. Download requires explicit `--download` and writes a bounded cache; CI reuses the same pin.
- [ ] Normalize selected Windows records with provider+EventID, source line, raw line SHA-256, record number, host, account domain, process GUID, PID, logon ID, and both collection and event clocks. Prefer Sysmon UtcTime; other EventTime values use explicit capture offset -04:00, an inference calibrated by Sysmon process-start pairs, never a universal timezone assumption. Expose second precision and ingestion delay.
- [ ] Decode bounded classic-PCAP Ethernet/IPv4 TCP/UDP headers and full single-packet WSMan HTTP request lines. Keep packet references and skip accounting. No stream reassembly, decryption, or interpretation of encrypted application content.
- [ ] Implement candidate rules: distinct-account failures grouped by host/caller/PID/session (5 in 15 seconds), distinct successful RC4 service-ticket requests per principal/client (5 in 15 seconds), IPC$/srvsvc accesses as context, and wsmprovhost→PowerShell process GUID parentage with same-host/logon/account evidence. Network corroboration uses exact IP/port tuples and bounded time; missing identity/session relationships remain explicit.
- [ ] Test before implementation: missing/invalid fields, archive integrity, UTC clocks, provider collision, same account in different domains, mapped IPv4, PID/host isolation, boundary thresholds, duplicate source records, matching parent GUIDs, mismatched sessions, packet truncation/fragmentation, missing network support. Validate full-capture output against a manually frozen source-reference oracle; do not claim population accuracy from one capture.
- [ ] Generate compact source excerpts, analysis JSON, CSV evidence table, and replay JSON/JS with provenance. Record license/credit and source hashes. Preserve all 25,993 host records in coverage accounting; browser evidence is a disclosed subset.

## Task 2 — Case and publication

- [ ] Write an analyst report with observations versus producer notes, correlation strength, time policy, competing legitimate-admin explanations, missing evidence, false-positive/false-negative limits, and reproducible commands.
- [ ] Add normalized-field SPL and Sigma candidate artifacts; distinguish unexecuted query translations from the executed Python analysis.
- [ ] Create `projects/ad-attack-chain.html` with phase selection, event-time/collection-time comparison, raw-field/source inspector, packet corroboration, detector logic, and linked report/downloads. Reuse existing replay controller and styles, keeping keyboard focus and reduced-motion/no-JS fallbacks.
- [ ] Add the case prominently to homepage/catalog/evidence directory/sitemap; preserve real captures and all other work. No fabricated Splunk or Wireshark screenshots.
- [ ] Run relevant unit, fixture and site checks; extend Chrome CI for the new route and both positive/negative inspector states. One independent source review and one batched desktop/mobile render review; fix material findings and verify.
- [ ] Update existing PR #13 with final implementation and verification. Integrate after green checks under the established portfolio publication workflow, then verify the live case/assets match the tested source.

## Review focus

Collection time is not event time. A missing 4625 source IP cannot become an invented client IP. Provider identities and account domains must survive normalization. PID-only, port-only, and time-only matches must not become causal evidence. Positive replay and negative counterexamples must both remain inspectable. Broader production claims and the unread LinkedIn honors remain outside this case.
