"""
Fabric IQ Agent — Semantic infrastructure & blast radius mapping.
Simulates Fabric IQ's ontology graph: maps the affected asset to connected
systems, data classifications, and ownership.
"""
import time


def run(alert_data: dict) -> dict:
    start = time.time()
    fabric = alert_data.get("fabric_iq", {})

    connected = fabric.get("connected_systems", [])
    blast_radius = fabric.get("blast_radius", "Unknown")
    owners = fabric.get("owners", [])
    graph = fabric.get("graph", {"nodes": [], "edges": []})
    citations = fabric.get("citations", [])

    # Reasoning: more connected systems with sensitive data = higher impact
    impact_signal = 10
    impact_signal += min(len(connected) * 15, 60)
    if any("DB" in c or "DATA" in c.upper() for c in connected):
        impact_signal += 20
    impact_signal = min(impact_signal, 100)

    findings = [f"Blast radius: {blast_radius}"]
    if owners:
        findings.append(f"System owner(s): {', '.join(owners)}")

    elapsed = round(time.time() - start, 2)

    return {
        "agent": "Fabric IQ Agent",
        "role": "Infrastructure Ontology & Blast Radius Mapping",
        "findings": findings,
        "citations": citations,
        "connected_systems": connected,
        "graph": graph,
        "impact_signal": impact_signal,  # 0-100
        "elapsed_seconds": elapsed,
    }