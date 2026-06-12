# SOCweave

> SOCweave — weaving threat intelligence, infrastructure data, and human
> context into one resolved verdict. Every time. Under 60 seconds.

**Built for Microsoft Agents League 2026 — Reasoning Agents Track**

## The Problem

SOC analysts spend 4–6 hours daily investigating security alerts that turn
out to be false positives. SOCweave eliminates that waste by reasoning like
a senior analyst — cross-examining technical evidence with human/organizational
context *before* reaching a verdict.

## What It Does

SOCweave is a **multi-agent reasoning system** with 5 distinct agent roles:

1. **Triage Orchestrator** — plans the investigation (visible "Reasoning Trace")
2. **Foundry IQ Agent** — grounds the alert against CVEs, MITRE ATT&CK, threat intel (cited)
3. **Fabric IQ Agent** — maps the infrastructure blast radius via a semantic ontology graph
4. **Work IQ Agent** — scans M365 emails/tickets for human authorization context
5. **Verdict Synthesizer (Critic)** — combines all signals into a confidence-scored
   verdict, with a self-correction loop if confidence is low

Each alert is resolved end-to-end — from raw alert to verified verdict with
remediation steps — in **under 60 seconds**.

## Architecture