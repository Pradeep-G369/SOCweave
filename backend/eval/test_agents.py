"""Unit tests for individual agent modules."""
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from agent import foundry_iq, fabric_iq, work_iq

def test_foundry_iq_detects_cve_match():
    alert = {"foundry_iq": {"cve_matches": ["CVE-2024-3094"], "threat_intel_matches": [], "external_ip_contacted": False, "citations": []}}
    result = foundry_iq.run(alert)
    assert result["malicious_signal"] >= 50
    assert "CVE-2024-3094" in result["findings"][0]

def test_foundry_iq_no_match_low_signal():
    alert = {"foundry_iq": {"cve_matches": [], "threat_intel_matches": [], "external_ip_contacted": False, "citations": []}}
    result = foundry_iq.run(alert)
    assert result["malicious_signal"] <= 20

def test_fabric_iq_blast_radius_scoring():
    alert = {"fabric_iq": {"connected_systems": ["DB-1", "DB-2"], "blast_radius": "test", "owners": [], "graph": {"nodes": [], "edges": []}, "citations": []}}
    result = fabric_iq.run(alert)
    assert result["impact_signal"] > 0

def test_work_iq_approved_ticket_raises_authorization():
    alert = {"work_iq": {"tickets": [{"id": "T1", "title": "test", "status": "Approved"}], "emails": [], "citations": []}}
    result = work_iq.run(alert)
    assert result["authorization_signal"] >= 50

def test_work_iq_no_evidence_zero_authorization():
    alert = {"work_iq": {"tickets": [], "emails": [], "citations": []}}
    result = work_iq.run(alert)
    assert result["authorization_signal"] == 0