# Evidence-first security case expansion

## Intent

Give an employer more first-party security work to inspect without turning the portfolio into a long list of unsupported claims. Replace the conceptual detection-engineering thumbnail on the home page with an existing genuine Splunk lab screenshot, complete three compact investigations with reproducible artifacts, and add an honest offensive-security experience page for the owner's prior Necromancer and HackThisSite training.

## Audience and outcome

The primary visitor is a recruiter, hiring manager, or SOC/security analyst reviewing Don Lopez for an entry-level cybersecurity role. Within a few minutes, the visitor should be able to identify the question investigated, inspect an actual result, follow the reasoning, and open the relevant evidence or code.

## Approaches considered

### 1. Experience narratives only

Add pages describing prior coursework and hacking practice without producing new artifacts. This is fastest, but repeats the portfolio's current weakness: claims without enough first-party evidence.

### 2. Recreate every historical course and VM lab

Rebuild the old classroom and CTF environments exactly. This would provide the strongest historical reconstruction, but the original VM images, screenshots, commands, and assignment briefs are unavailable. The current workspace also has no hypervisor. Exact recreation would be expensive and could introduce invented details.

### 3. Evidence-first hybrid — selected

Run new, safe, deterministic investigations now and preserve their inputs, outputs, reports, hashes, and visual results. Present Necromancer and HackThisSite as owner-confirmed prior training with official platform references, while avoiding invented flags or commands. This adds proof now and keeps historical claims within the evidence available.

## Selected scope

### Home-page proof upgrade

- Replace the conceptual detection-engineering SVG shown in the supplied screenshot with the existing genuine Splunk result screenshot.
- Keep its `Actual lab screenshot` label and link it to the broader detection-engineering story.
- Add one new investigation card to the home page only if it improves the scan path; the complete set belongs on `explore.html`.

### Completed phishing-email investigation

- Convert the existing planned phishing brief into a completed, reproducible case.
- Use a harmless deterministic `.eml` fixture created for the lab.
- Preserve the message hash, parsed headers, sender/Reply-To comparison, authentication indicators, extracted URL/domain, findings, limitations, and response recommendation.
- Include a visual produced from the actual analyzer result and links to the fixture, analyzer, machine-readable result, and case report.
- Connect the case to completed IST 5250 Incident Handling & Cyber Investigation coursework without claiming it was a specific archived class assignment.

### Completed enterprise-account investigation

- Build a deterministic account-activity fixture representing repeated failures, a later successful sign-in, and a privileged group-change event.
- Preserve the event timeline, detection logic, severity reasoning, alternative explanations, and containment recommendations.
- Include a visual produced from the actual analysis and links to the inputs, analyzer, result, and report.
- Connect the case to completed IST 4910 Enterprise Systems Administration and IST 5250 coursework without claiming historical assignment details.

### Completed web attack-log investigation

- Run a local-only web service and send a small, predeclared set of benign and attack-pattern requests to it.
- Preserve the actual access log, request manifest, analyzer output, findings, and remediation recommendations.
- Do not contact, scan, or test a public target.
- Connect the case to completed IST 5930 Web System Security and IST 5250 coursework.

### Offensive-security and VM training

- Add an `Offensive Security & VM Labs` page describing owner-confirmed use of Kali, VMware, the VulnHub Necromancer boot-to-root VM, and HackThisSite training missions.
- Cite VulnHub's official Necromancer page and HackThisSite's official description of its legal training environment.
- Use the existing attributed Kali reference image until a personal VM screenshot is supplied.
- Do not invent completed flag counts, exact exploit steps, dates, scores, usernames, or mission names.
- Explain the transferable workflow: isolate the target, enumerate, validate a path, document evidence, and translate offensive activity into defender-visible telemetry.

### Digital-forensics evidence upgrade

- Replace the generic forensic-hardware photograph on the E3 page and home card with a result produced by a newly executed, reproducible forensic evidence examination.
- Preserve the original evidence hash, working-copy hash, artifact inventory, timeline, finding references, and examiner-style report.
- Present Paraben E3 as owner-confirmed classroom tool experience, while making clear that the newly published analysis is an independent reproducible lab rather than a recovered E3 screenshot.
- Credit Chuck Easttom's *Digital Forensics, Investigation, and Response, Fourth Edition* as a methodology source the owner used. Apply its high-level collect, analyze, present, minimize-original-handling, analysis-plan, and documented-findings principles without reproducing copyrighted book text or claiming the new lab was an archived book assignment.

## Evidence and image language

- Use `Actual lab screenshot` only for the existing genuine Splunk capture.
- Use `Reproducible lab result` for visuals generated from newly executed analyzers.
- Use `Attributed reference image` for third-party imagery.
- Use `Owner-confirmed prior training` for Necromancer and HackThisSite experience without surviving first-party artifacts.
- Do not call any item `fake`. Generated fixtures must still be identified as `synthetic` or `lab-created` where needed to prevent a false production-incident claim.
- Do not use AI-generated imagery as evidence.
- Replace the current E3 reference photograph in employer-facing case cards; retain its credit only if the asset remains distributed for another documented purpose.

## Information architecture

- Keep the home page concise: four or five strongest investigations, then a link to all work.
- Put the expanded case catalog and status labels on `explore.html`.
- Every completed case follows the same reading order: question, evidence visual, timeline/workflow, findings, limitations, downloadable artifacts, academic foundation, and scope.
- Add the new cases to `projects/CASE_STUDIES.md` and repository documentation.

## Visual direction

Preserve the existing restrained cream/green portfolio identity. Evidence panels should look like analyst work surfaces rather than decorative cybersecurity art: readable timestamps, event relationships, hashes, concise findings, and one strong result per visual. Motion is optional and must explain progression; no ambient hacker animation is added.

## Constraints and anti-goals

- Preserve the current résumé PDF and private transcript unchanged and unpublished.
- The transcript verifies degree, course completion, terms, and honors; it does not verify particular assignments, tools, or lab outcomes.
- Do not represent lab data as a real victim, production system, employer incident, or historical school submission.
- Do not reproduce a historical VM compromise without the VM and its evidence.
- No external scanning, credential use, live exploitation, or interaction with public targets is required.
- Keep all new cases deterministic, offline-capable, and inexpensive to rerun.

## Verification

- Write evidence-contract checks before implementation so planned/completed status and labels cannot drift.
- Execute each new lab from a clean state and verify stable outputs and hashes.
- Run the repository's complete checks, accessibility/link validation, and site packaging.
- Review desktop, mobile, and small-mobile captures once; make at most one bounded visual correction pass.
- Publish only after the exact reviewed head passes CI and the live-site verifier.

## Deferred evidence

Personal Necromancer, HackThisSite, VMware, E3, and original five-rule screenshots can replace reference or summary visuals later if the owner supplies them. Their absence does not block the new reproducible investigations.
