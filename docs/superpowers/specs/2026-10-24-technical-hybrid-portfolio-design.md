# Technical hybrid portfolio design

Status: selected direction; detailed design for review. No website implementation in this change.

## Intent and audience

Help a SOC hiring manager understand Don Lopez's analysis quickly, then let a technical interviewer inspect the events, rules, assumptions, and evidence underneath. Replace weak illustrations and shallow stage diagrams with meaningful motion while retaining genuine images and completed experience.

The owner selected the hybrid direction on October 24, 2026 and explicitly reinforced retaining live images and the earlier portfolio requirements. This design records that selection without treating newly proposed functionality as already implemented.

## Approaches and selection

| Approach | Strength | Cost or limitation |
| --- | --- | --- |
| Guided walkthrough | Fast, clear explanation | Little independent inspection |
| Full technical workbench | Deep exploration of data and code | Too demanding as the first encounter |
| Selected: hybrid | Readable animated overview plus optional technical inspection | Needs consistent evidence and playback behavior |

## Existing context

Reviewed baseline: `7534bb1a6e0cc8cf23b528216813ffcec5106bd2` on the public portfolio repository. Static HTML, `portfolio.css`, and plain JavaScript; no frontend dependency installation is needed. Existing `portfolio-systems.js` exports `evaluateCR` and `evaluateRAI`; preserve those APIs and their tests while introducing richer independent examples. Existing `signal-display.js` animates a decorative path, not an investigation.

## Carry-forward requirements

- Preserve the white, charcoal, and forest-green visual identity; retain the dark green Signal to Case panel.
- Keep actual lab images, real campus photographs, readable explanations, existing case routes, résumé downloads, source links, and reproduction guides.
- Preserve completed Kali/VMware, Necromancer, HackThisSite, networking, Wireshark, Snort, and Splunk experience. Do not turn previously completed experience back into a planned project.
- Preserve phishing, enterprise account/MFA, web attack-log, Windows triage, and packet investigations. Add paths into these cases from the relevant technical inspectors rather than duplicating their results.
- Preserve the forensic examination and its integrity hashes, working-copy method, artifact citations, timeline, E3 classroom context, and the method reference to *Digital Forensics, Investigation, and Response, Fourth Edition*.
- Keep education and campus imagery, Security+, CySA+, and the planned Splunk SCCDA credential. Do not alter either résumé PDF or expose the transcript.
- Show genuine captures and explanatory animations together. “Live images” means actual captured interfaces or photographs where available; the static website must not imply a connected monitoring feed.
- No invented original lab screenshots, event sets, exploit outcomes, production incidents, accuracy, or employment claims. Keep the reported 5+ rules and approximately 30% false-positive reduction separate from the smaller public authentication exercise.

## Visual and interaction direction

Visitor mode: Experience on the homepage, Read plus optional Operate on case pages. The first view explains an actual engineering decision; selecting “Inspect logic” opens its event and code detail. Keep prose readable and technical payloads in monospace tables or code blocks. Use teal for selected relationships, amber for review/uncertainty, and text labels for every state. Avoid adding a dashboard shell to the entire portfolio.

On desktop, use a visual beside a short explanation, followed by a genuine evidence image strip and links. Case workbenches use an overview above a two-column event/code inspector. On mobile, stack overview, controls, selected-event summary, then details; allow horizontal scrolling inside code/tables only. No hover-only information. Keep captions outside images and screenshots uncropped enough to read; open original image on selection.

Motion is finite and user-controlled. Play, Pause, Step, and Reset must describe the sequence. Selecting an item pauses playback. Pause offscreen and when the document is hidden; do not unexpectedly restart. Reduced-motion mode keeps step and inspection controls available without travelling effects. Without JavaScript, show a complete representative state, captions, code excerpts, and normal links.

## 1. Detection Engineering & Rule Development

Replace the homepage detection thumbnail with a compact animated event timeline, then retain the actual Splunk capture immediately below/alongside it as evidence. Expand `projects/detection-engineering.html` into a rule laboratory with a short explanation followed by inspectable implementation.

### First implementation: authentication boundary

Use the existing 64-event, nine-scenario corpus and expected findings as the authority. Build browser-readable data from those files; do not hand-author a second copy of counts or timestamps. Show threshold, below-threshold, success-reset, different-user, different-IP, expired-window, boundary, and interleaved cases through a scenario selector.

The centerpiece is the inclusive window at a success event: `0 <= success_time - failure_time <= 600`, with at least five preceding failures in the same username/source-IP streak since the prior success. Explain that host is context, not a grouping key in the current rule. Stable input order resolves equal timestamps in the public fixture; this is a documented modeling choice, not an assurance about arbitrary ingestion order.

Selecting an event shows timestamp, username, source IP, host, event type, scenario, age at success, and inclusion/exclusion reason. A window overlay moves over the timeline; excluded events remain visible. An intervening success resets the streak. Never infer an alert from failures belonging to a different account or source address.

The inspector has four sections:

1. **Behavior and telemetry:** hypothesis, required fields, UTC parsing, ordering, grouping, missing-data behavior, and required log coverage.
2. **Actual logic:** readable excerpts from the committed SPL and Python implementation, with source links and an explanation of each material operation. Label browser evaluation as JavaScript replay of this public fixture; it does not execute Splunk.
3. **Validation:** expected/observed findings and individual failures. The observed historical comparison is 3/5 to 5/5 on this training set. Keep saved-panel observation separate from automated browser test output and from indexed ingestion or alert firing, which were not verified.
4. **Tuning and limitations:** boundary correction, grouping/reset behavior, benign alternatives, false-positive/false-negative tradeoffs, and additional evidence needed for disposition.

Encoded PowerShell is a technical companion linked to `windows-process-triage.html`: explain process ancestry, command line, decoded content where available, and legitimate administration as a competing explanation. Lateral movement is linked completed experience with its artifact availability stated. Do not create fake finished rule collections or imply that encoding alone proves maliciousness. A generic example may be authored only if clearly distinguished from the original work.

## 2. Celestial Resonance

Replace “Follow a research input” with “Inspect a point-in-time dataset.” Show a two-lane version timeline: observation time and version availability. The focal interaction changes the decision cutoff and reveals which version enters a research dataset, plus the precise reason each other version is excluded.

Use a small, explicitly fictional public fixture with fields `record_id`, `observation_time`, `available_at`, `vintage_id`, `value`, and `source_hash`. The hash is computed from the canonical fixture bytes and labeled a fixture hash; do not fabricate a private CR receipt. A separate `decision_time` is an input. Accept equality at the cutoff. Require both observation and availability at/before the cutoff. Resolve the latest eligible vintage only after validation; conflicting records tied at the latest availability time produce an ambiguity hold.

A selectable record opens a field inspector and decision trace: schema validation, time eligibility, vintage selection, and dataset inclusion. Keep eligible, not-yet-available, future-observation, superseded, and ambiguous states distinct. The receipt names the fixture version, selected IDs, cutoff, and exclusions. The displayed hash identifies the source fixture; it is not presented as a full experiment identity. No forecasting or private CR code executes.

The story must also explain acquisition, preserved snapshots, normalization, availability versus observation, reproducibility, and why comparisons need frozen inputs. Forecasting remains the project objective, not a proven performance claim. The animation is a portfolio explanation, not a substitute for the private project's verification.

## 3. Research AI Infrastructure

Replace the two-box agreement exercise with a small claim/evidence graph backed by four authored public scenarios: supported, contradictory, missing coverage, and incorrect attribution. Each has a visible claim, two or three short source records, source IDs, passage IDs, measurement scope, dates, and exact source text. These remain fictional examples independent of private RAI.

Selecting a claim highlights its cited passages and the transformation to the answer. Selecting an edge explains its relation. A source inspector exposes the actual passage, reference, period, and scope. Do not implement arbitrary-prose verification or call the exercise a general truth checker.

The scope example initially presents a potential disagreement. Inspection reveals different periods or measurements, so the outcome is “not directly comparable”; the answer narrows its wording rather than claiming consensus or automatically resolving the scientific question. A separate true-conflict fixture retains comparable contradictory observations.

The technical explanation covers retrieval candidates versus cited support, provenance, evidence coverage, citation attribution, contradiction, and bounded answers. No decorative probability or model confidence percentage. Keep RAI independent of CR and do not activate either private system.

## 4. Signal to Case

Keep the existing name and dark panel, replacing generic icons with an event-to-disposition replay. The homepage summary has four selectable stages: **Events**, **Rule**, **Context**, **Disposition**. Preserve the breadth of the lab path with small, accurate labels for Kali/VMware, network visibility, Splunk, and case documentation.

The default replay uses the public authentication boundary scenario, not invented cross-source findings:

1. Timestamped source events arrive with an explicit case/scenario identity.
2. The inclusive rule window selects the relevant failures and success.
3. Account and network/endpoint context is marked as present, absent, or needed; missing context remains missing. Link to the independent packet and Windows cases without merging their artifacts into this authentication incident.
4. The disposition is “Investigate: suspicious authentication sequence; compromise not established,” with linked event IDs, rule source, and the next useful checks.

A below-threshold fixture is the counterexample and says “Rule not triggered,” not “benign confirmed.” Explain that a benign disposition needs supporting context; do not turn absence of an alert into proof of safety. The event inspector opens on click/keyboard selection; an “Open full investigation” link routes to the existing case. Replay starts only on request and ends at disposition.

## Genuine image and evidence placement

| Asset / case | Placement and role | Scope to retain |
| --- | --- | --- |
| `assets/evidence/splunk-native-dashboard-results.png` | Detection and Splunk evidence drawer; full-size link | Actual cropped saved panel using synthetic events; not proof of alert firing |
| Three `assets/reference/csusb-*.webp` images | Existing academic gallery and education link | Attributed photographs; preserve credits |
| `assets/reference/kali-desktop-2020.4.png` | VM experience reference gallery, secondary to technical walkthrough | Attributed Kali desktop reference, not owner's recovered session |
| `assets/network/*.svg` | Packet case evidence references | Generated views of the reproducible public fixture, not application captures |
| Phishing/account/web/forensic evidence SVGs | Corresponding case links/drawers | Reproducible result visualizations, not tool screenshots |
| `assets/artwork/*.webp` | Remove from leading evidence slots when replaced | Generated editorial artwork must never be relabeled as evidence |

Retain existing real images immediately. If new owner-original captures become available, add them beside their relevant case with source/date and sensible redaction. Missing original captures do not block the redesign and do not justify generated substitutes. Do not fabricate a Wireshark, Snort, E3, Necromancer, or HackThisSite session screenshot.

## Build boundaries and acceptance

Use static HTML/CSS/plain JavaScript; no framework, new runtime dependency, live service, external API, private-source publication, or backend change. Preserve existing demo APIs and compatibility anchors. Build a shared replay controller only for the repeated playback behavior; each workbench owns its data and decisions.

Acceptance: the visitor can inspect an event's rule inclusion, reproduce exact-boundary handling, inspect a vintage decision with explicit exclusions, follow a claim to an exact passage, and distinguish an investigation lead from a confirmed compromise. Real images remain discoverable at useful size. All existing cases and source links remain reachable without JavaScript. Controls work with keyboard, reduced motion, and mobile. Validate changed behavior against the committed fixtures, then inspect desktop/mobile once, batch fixes, and confirm once if necessary.

## Builder choices and delivery

Builder may choose SVG geometry, exact spacing, and minor copy within the established identity. Use semantic controls and local SVG/data-driven rendering; do not generate bitmap replacements for technical diagrams. Preserve factual metrics and source boundaries. Suggested implementation tasks: fixture-backed detection/replay; CR/RAI inspectors; image integration and responsive verification.

The owner approved the hybrid concept; this detailed spec and its implementation plan are the concrete review artifacts. This documentation-only change does not update the deployed website.
