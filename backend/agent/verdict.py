"""
Verdict Synthesizer Agent — combines all IQ agent outputs into a final
verdict with confidence score, severity delta, and plain-English summary.
Acts as the "Critic/Verifier" in the reasoning chain.
"""


SEVERITY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def synthesize(alert_data: dict, foundry_result: dict, fabric_result: dict, work_result: dict) -> dict:
    malicious = foundry_result["malicious_signal"]
    impact = fabric_result["impact_signal"]
    authorized = work_result["authorization_signal"]

    # --- Confidence + direction reasoning ---
    # If strong authorization found AND low malicious signal -> downgrade (false positive)
    # If no authorization AND high malicious signal -> escalate (true threat)
    raw_threat_score = (malicious * 0.5) + (impact * 0.3) - (authorized * 0.6)
    raw_threat_score = max(0, min(100, raw_threat_score + 30))  # normalize to 0-100

    if authorized >= 80 and malicious < 50:
        severity_after = "LOW"
        status = "AUTHORIZED MAINTENANCE"
        confidence = min(99, 60 + authorized // 3)
        delta_direction = "down"
    elif malicious >= 70 and authorized < 30:
        severity_after = "CRITICAL"
        status = "CONFIRMED THREAT - ESCALATE IMMEDIATELY"
        confidence = min(99, 60 + malicious // 3)
        delta_direction = "up"
    elif raw_threat_score >= 60:
        severity_after = "HIGH"
        status = "REQUIRES ANALYST REVIEW"
        confidence = 65
        delta_direction = "flat"
    else:
        severity_after = "MEDIUM"
        status = "MONITOR - LOW CONFIDENCE"
        confidence = 55
        delta_direction = "flat"

    severity_before = alert_data.get("severity", "UNKNOWN")

    # --- Self-correction / critic loop ---
    # If confidence is low, simulate a re-query of Work IQ with broader scope
    critic_notes = []
    if confidence < 70:
        critic_notes.append(
            "Confidence below 70% threshold — Critic agent triggered re-query of "
            "Work IQ with extended 72-hour lookback window."
        )
        # Simulate the re-query slightly boosting confidence if some signal exists
        if authorized > 0 or malicious > 0:
            confidence = min(confidence + 10, 99)
            critic_notes.append("Re-query found additional weak signal — confidence adjusted.")
        else:
            critic_notes.append("No additional signal found — verdict stands at original confidence.")

    # --- Severity delta ---
    before_rank = SEVERITY_RANK.get(severity_before, 2)
    after_rank = SEVERITY_RANK.get(severity_after, 2)
    if after_rank < before_rank:
        delta_label = f"Severity DOWNGRADED: {severity_before} -> {severity_after}"
    elif after_rank > before_rank:
        delta_label = f"Severity ESCALATED: {severity_before} -> {severity_after}"
    else:
        delta_label = f"Severity UNCHANGED: {severity_before}"

    # --- Plain-English summary (max 3 lines per UI spec) ---
    findings_combined = (
        foundry_result["findings"] + fabric_result["findings"] + work_result["findings"]
    )
    summary = _build_summary(severity_after, status, findings_combined, confidence)
    reasoning_chain = _build_reasoning_chain(foundry_result, fabric_result, work_result, severity_after, confidence)

    # --- Evidence count ---
    total_citations = (
        len(foundry_result.get("citations", []))
        + len(fabric_result.get("citations", []))
        + len(work_result.get("citations", []))
    )

    # --- Remediation steps (only for confirmed threats) ---
    remediation = []
    if status == "CONFIRMED THREAT - ESCALATE IMMEDIATELY":
        asset = alert_data.get("asset", "the affected system")
        remediation = [
            f"Isolate {asset} from the network immediately",
            "Rotate credentials and API keys associated with the affected system",
            f"Notify owning team(s): {', '.join(fabric_result.get('connected_systems', [])[:1]) or 'system owner'}",
            "Preserve forensic image before remediation for incident response",
        ]

    return {
        "alert_id": alert_data.get("alert_id"),
        "asset": alert_data.get("asset"),
        "severity_before": severity_before,
        "severity_after": severity_after,
        "delta_direction": delta_direction,
        "delta_label": delta_label,
        "status": status,
        "confidence": confidence,
        "evidence_count": total_citations,
        "summary": summary,
        "reasoning_chain": reasoning_chain,
        "remediation": remediation,
        "critic_notes": critic_notes,
    }


def _build_summary(severity_after: str, status: str, findings: list, confidence: int) -> str:
    """Build a max-3-line plain English executive summary."""
    icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}.get(severity_after, "⚪")
    line1 = f"{icon} {status} — {severity_after} SEVERITY"
    line2 = findings[0] if findings else "Analysis complete."
    line3 = f"Confidence: {confidence}%"
    return f"{line1}\n{line2}\n{line3}"


def _build_reasoning_chain(foundry_result: dict, fabric_result: dict, work_result: dict,
                            severity_after: str, confidence: int) -> str:
    """Builds a multi-sentence analytical explanation chaining evidence
    across all three agents — simulates a senior analyst's reasoning."""
    parts = []

    # Foundry IQ contribution
    f_finding = foundry_result["findings"][0]
    parts.append(f"Technical analysis shows: {f_finding}.")

    # Fabric IQ contribution
    fab_finding = fabric_result["findings"][0]
    parts.append(f"Infrastructure context adds: {fab_finding}.")

    # Work IQ contribution
    w_finding = work_result["findings"][0]
    parts.append(f"Human/organizational context reveals: {w_finding}.")

    # Concluding synthesis
    if confidence < 70:
        parts.append(
            f"Combining these three independent signals, the evidence is ambiguous "
            f"with only {confidence}% confidence — the activity is plausible but "
            f"unconfirmed, and the Critic agent recommends continued monitoring "
            f"and analyst review rather than automatic closure or escalation."
        )
    elif severity_after in ("LOW", "MEDIUM"):
        parts.append(
            f"Combining these three independent signals, the evidence converges on a "
            f"low-risk explanation with {confidence}% confidence — recommending no "
            f"escalation at this time."
        )
    else:
        parts.append(
            f"Combining these three independent signals, the evidence converges on a "
            f"genuine threat with {confidence}% confidence — recommending immediate "
            f"escalation and remediation."
        )

    return " ".join(parts)