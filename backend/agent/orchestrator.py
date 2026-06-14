"""
Triage Orchestrator Agent — the planner/coordinator of the multi-agent
system. Builds an execution plan (visible to the UI as the "Reasoning
Trace"), invokes each IQ agent in sequence, tracks timing for the audit
trail, and hands off to the Verdict Synthesizer.
"""
import time
import logging
logger = logging.getLogger(__name__)
from agent import foundry_iq, fabric_iq, work_iq, verdict
from safety.sanitize import sanitize_alert
from safety.clean_data import scrub_pii


def get_plan() -> list[str]:
    """Returns the orchestrator's reasoning plan (shown in UI before execution)."""
    return [
        "Sanitize and validate incoming alert payload",
        "Scrub PII from human-context data before processing",
        "Query Foundry IQ for CVE / MITRE ATT&CK / threat-intel grounding",
        "Query Fabric IQ for infrastructure blast-radius mapping",
        "Query Work IQ for human authorization context (tickets/emails)",
        "Synthesize verdict: confidence score + severity delta",
        "Critic check: if confidence < 70%, trigger re-query loop",
        "Generate remediation plan (if confirmed threat)",
    ]


def run_pipeline(alert_data: dict) -> dict:
    pipeline_start = time.time()
    logger.info(f"Processing alert: {alert_data.get('alert_id')} | severity: {alert_data.get('severity')}")
    audit_trail = []

    # Step 1: Sanitize input
    t0 = time.time()
    alert_data = sanitize_alert(alert_data)
    audit_trail.append(_step("Alert Ingested & Sanitized", t0))

    # Step 2: Scrub PII
    t0 = time.time()
    alert_data = scrub_pii(alert_data)
    audit_trail.append(_step("PII Scrubbed from Human-Context Data", t0))

   # Step 3: Foundry IQ
    t0 = time.time()
    try:
        foundry_result = foundry_iq.run(alert_data)
        audit_trail.append(_step("Foundry IQ: Threat Intelligence Grounding", t0))
    except Exception as e:
        foundry_result = {"agent": "Foundry IQ Agent", "role": "Technical Grounding", "findings": [f"Agent error: {str(e)}"], "citations": [], "malicious_signal": 0, "elapsed_seconds": 0}
        audit_trail.append(_step(f"Foundry IQ: ERROR — {str(e)}", t0))

    # Step 4: Fabric IQ
    t0 = time.time()
    try:
        fabric_result = fabric_iq.run(alert_data)
        audit_trail.append(_step("Fabric IQ: Blast Radius Mapping", t0))
    except Exception as e:
        fabric_result = {"agent": "Fabric IQ Agent", "role": "Infrastructure Ontology", "findings": [f"Agent error: {str(e)}"], "citations": [], "connected_systems": [], "graph": {"nodes": [], "edges": []}, "impact_signal": 0, "elapsed_seconds": 0}
        audit_trail.append(_step(f"Fabric IQ: ERROR — {str(e)}", t0))

    # Step 5: Work IQ
    t0 = time.time()
    try:
        work_result = work_iq.run(alert_data)
        audit_trail.append(_step("Work IQ: Human Context & Authorization Scan", t0))
    except Exception as e:
        work_result = {"agent": "Work IQ Agent", "role": "Human Context", "findings": [f"Agent error: {str(e)}"], "citations": [], "authorization_signal": 0, "elapsed_seconds": 0}
        audit_trail.append(_step(f"Work IQ: ERROR — {str(e)}", t0))

    # Step 6 + 7: Verdict synthesis (includes critic loop)
    t0 = time.time()
    final_verdict = verdict.synthesize(alert_data, foundry_result, fabric_result, work_result)
    audit_trail.append(_step("Verdict Synthesis & Critic Check", t0))

    total_elapsed = round(time.time() - pipeline_start, 2)
    logger.info(f"Alert {alert_data.get('alert_id')} resolved: {final_verdict.get('status')} | confidence: {final_verdict.get('confidence')}%")

    return {
        "plan": get_plan(),
        "audit_trail": audit_trail,
        "agents": {
            "foundry_iq": foundry_result,
            "fabric_iq": fabric_result,
            "work_iq": work_result,
        },
        "verdict": final_verdict,
        "total_elapsed_seconds": total_elapsed,
    }


def _step(name: str, start_time: float) -> dict:
    return {
        "step": name,
        "status": "complete",
        "elapsed_seconds": round(time.time() - start_time, 3),
    }