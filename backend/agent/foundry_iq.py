"""
Foundry IQ Agent — Grounded technical threat intelligence.
Simulates Foundry IQ's agentic retrieval: returns cited findings about
CVEs, MITRE ATT&CK techniques, and threat-intel IP matches.
"""
import time


def run(alert_data: dict) -> dict:
    """
    Input: full alert dict (contains 'foundry_iq' mock retrieval results)
    Output: structured findings + citations + a verdict_signal (0-100,
            higher = more malicious)
    """
    start = time.time()
    fiq = alert_data.get("foundry_iq", {})

    cve_matches = fiq.get("cve_matches", [])
    threat_matches = fiq.get("threat_intel_matches", [])
    external_ip = fiq.get("external_ip_contacted", False)
    citations = fiq.get("citations", [])

    # Reasoning: score based on evidence found
    signal = 10  # baseline
    if cve_matches:
        signal += 40
    if threat_matches:
        signal += 35
    if external_ip:
        signal += 15

    signal = min(signal, 100)

    findings = []
    if cve_matches:
        findings.append(f"Matched known CVE(s): {', '.join(cve_matches)}")
    if threat_matches:
        findings.append(f"Threat intel match: {threat_matches[0]}")
    if not cve_matches and not threat_matches:
        findings.append("No CVE or threat-intel matches found for this activity pattern")

    elapsed = round(time.time() - start, 2)

    return {
        "agent": "Foundry IQ Agent",
        "role": "Technical Grounding & Threat Intelligence",
        "findings": findings,
        "citations": citations,
        "malicious_signal": signal,  # 0-100
        "elapsed_seconds": elapsed,
    }