# Synthetic Network Threat-Hunting Case — LAB-NET-001

**Prepared by:** Don Lopez  
**Classification:** Fabricated educational example, **not an actual incident**  
**Source:** 20-packet PCAP generated offline by the published Python script  
**Disposition:** `SYNTHETIC_TRIAGE_ONLY`

## Question

What do repeated unsuccessful DNS lookups and a subsequent HTTP POST in fabricated network telemetry actually establish?

## Synthetic timeline (2026-10-10 UTC)

| UTC time | Source | Observation | Evidence interpretation |
| --- | --- | --- | --- |
| 12:00:00–12:00:36.200 | `192.0.2.10` → `198.51.100.53` | Four matched DNS questions and NXDOMAIN replies for `bad-1.invalid` through `bad-4.invalid` | Failed-name pattern meets review threshold; no tunneling payload was observed |
| 12:00:48–12:00:48.200 | `192.0.2.11` | Successful `portal.example` lookup | Benign comparison |
| 12:01:00–12:01:00.040 | `192.0.2.11` → `203.0.113.80` | TCP handshake, GET `/index.html`, HTTP 200 | Benign comparison |
| 12:01:15–12:01:15.040 | `192.0.2.10` → `203.0.113.80` | TCP handshake, POST to `collector.invalid/upload`; body is literal `SAFE` | Rule match only; no real data transfer to an external service |

## Observations and hypotheses

**What the fabricated PCAP demonstrates:** Exactly 20 encoded frames, 12 decoded events and two rule matches with fixed timestamps. The SHA-256 of the generator output is `5fc309499252677ba5cd31106b611edde5fd1b941aed3cc2f87f216da4dd707c`.

**What it does not demonstrate:** DNS tunneling, command-and-control, malicious process attribution, stolen information, an unauthorized upload, or any production incident. ATT&CK T1071.004 (DNS) and T1071.001 (Web Protocols) provide investigative context only.

**Alternatives and missing evidence:** Application misconfiguration or negative-cache effects can cause repeated NXDOMAIN; HTTP POST is routine in legitimate software. We lack endpoint process association, real resolver logs, proxy and TLS records, destination ownership, user intent and behavioral baselines.

## Verification and handoff

Recreate the PCAP, verify its digest, execute the analyzer, compare its two findings to [expected_findings.json](expected_findings.json) and run 18 unit tests. The parser has already passed those tests locally; **an actual Wireshark GUI inspection is not claimed**.

In authorized enterprise work, identify the originating process, check DNS query characteristics and baselines, examine proxy/eDR correlations, and determine whether endpoint/identity evidence supports escalation. Obtain required permissions before active response.

**Disposition:** Keep as a synthetic training example; no real attack or exfiltration established.
