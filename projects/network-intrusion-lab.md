# Network Intrusion Investigation

Use packet evidence and IDS rules to investigate activity in an isolated lab.

Kali Linux · Wireshark · Snort · 2025

Résumé lab: 5,000+ packets analyzed, with Snort rule implementation and tuning.

## The investigation problem

A scan, repeated connection attempt or unusual application request needs context. Packet analysis makes the exchange inspectable; an IDS rule turns a chosen pattern into a repeatable signal. Neither removes the need for an analyst to explain the behavior.

## My lab work

My résumé describes simulating scanning, brute-force and exploitation activity in a Kali Linux lab, analyzing more than 5,000 packets in Wireshark, and implementing and tuning Snort rules for the simulated attacks.

The case will pair the original packet evidence with the corresponding rule and alert context. The smaller generated DNS/HTTP exercise already in this portfolio is a separate investigation.

## From packet to finding

- **Bound the scenario.** Identify the lab systems, activity and capture interval.
- **Inspect the exchange.** Use protocol fields and conversation timing to explain the observed behavior.
- **Compare the alert.** Relate the Snort predicate and triggering traffic, and consider legitimate matches.
- **Document the conclusion.** Preserve packet references, rule context, limitations and the recommended next step.

## What a useful case report contains

A readable timeline, relevant Wireshark filters, packet references, the Snort rule, the alert it produced and an explanation of what tuning changed. Screenshots should support the reasoning rather than substitute for it.

## A public packet exercise

The generated 20-frame PCAP demonstrates DNS and HTTP analysis with a deterministic analyzer and expected findings. It is immediately inspectable, but it is not the original 5,000+ packet lab.

[Explore the generated packet case ↗](network-traffic-analysis.md)

## Scope and evidence

Completed lab work described in my supplied résumé. The original lab artifacts and screenshots will be added here; the linked public exercises have their own, smaller scope. This is lab experience, not a claim of a production incident or paid SOC employment.

Background reference

[MITRE ATT&CK: credential attack context ↗](https://attack.mitre.org/techniques/T1110/). This reference informs the investigation approach; it does not verify my lab results.

[Choose another case study ↗](../explore.html)
