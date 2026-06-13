"""
Analyst Co-Pilot — uses spaCy semantic similarity (offline NLP/ML) to
match the analyst's question to the right evidence category, then
returns relevant findings from the agent results.
"""
import spacy

try:
    _nlp = spacy.load("en_core_web_lg")
    _NLP_AVAILABLE = True
except Exception:
    _nlp = None
    _NLP_AVAILABLE = False

# Reference questions for each category - the analyst's question is
# compared against these using semantic similarity
_CATEGORIES = {
    "reasoning": "why did the severity change, explain the verdict reasoning",
    "evidence": "show me the evidence, citations, and sources",
    "work": "were there any emails or tickets authorizing this activity",
    "fabric": "what systems are connected, what is the blast radius impact",
    "foundry": "are there any known threats, CVEs, or malicious indicators",
    "confidence": "how confident is this verdict",
    "remediation": "what actions or remediation steps should be taken next",
}


def answer_question(question: str, context: dict) -> str:
    verdict = context.get("verdict", {})
    agents = context.get("agents", {})

    foundry = agents.get("foundry_iq", {})
    fabric = agents.get("fabric_iq", {})
    work = agents.get("work_iq", {})

    category = _classify(question)

    if category == "reasoning":
        return verdict.get("reasoning_chain", "No reasoning available.")

    if category == "evidence":
        all_citations = (
            foundry.get("citations", []) + fabric.get("citations", []) + work.get("citations", [])
        )
        return "Evidence sources: " + "; ".join(all_citations)

    if category == "work":
        findings = work.get("findings", [])
        if findings:
            return "Work IQ findings: " + "; ".join(findings)
        return "No email or ticket evidence was found for this alert."

    if category == "fabric":
        findings = fabric.get("findings", [])
        return "Fabric IQ findings: " + "; ".join(findings)

    if category == "foundry":
        findings = foundry.get("findings", [])
        return "Foundry IQ findings: " + "; ".join(findings)

    if category == "confidence":
        return f"The confidence score is {verdict.get('confidence')}%, based on combined signals from all three IQ agents."

    if category == "remediation":
        remediation = verdict.get("remediation", [])
        if remediation:
            return "Recommended actions: " + "; ".join(remediation)
        return "No remediation actions are needed — this alert was resolved as low-risk."

    return (
        "I can answer questions about: why the verdict changed, evidence/citations, "
        "blast radius, threat intel (CVE/MITRE), authorization (emails/tickets), "
        "confidence score, or remediation steps. Try rephrasing your question."
    )


def _classify(question: str) -> str | None:
    """Classifies the question into a category using spaCy semantic
    similarity. Falls back to keyword matching if spaCy unavailable."""
    if _NLP_AVAILABLE:
        try:
            q_doc = _nlp(question.lower())
            best_category, best_score = None, 0.0
            for cat, ref_text in _CATEGORIES.items():
                ref_doc = _nlp(ref_text)
                score = q_doc.similarity(ref_doc)
                if score > best_score:
                    best_score, best_category = score, cat
            if best_score > 0.55:  # similarity threshold
                return best_category
        except Exception:
            pass

    # Fallback: keyword matching
    return _keyword_classify(question)


def _keyword_classify(question: str) -> str | None:
    q = question.lower()
    if any(w in q for w in ["why", "reason", "explain", "downgrad", "escalat", "verdict", "change"]):
        return "reasoning"
    if any(w in q for w in ["evidence", "citation", "source", "proof"]):
        return "evidence"
    if any(w in q for w in ["email", "ticket", "authoriz", "approv", "work"]):
        return "work"
    if any(w in q for w in ["blast", "infrastructure", "connected", "impact", "fabric"]):
        return "fabric"
    if any(w in q for w in ["cve", "threat", "mitre", "malicious", "foundry"]):
        return "foundry"
    if "confidence" in q:
        return "confidence"
    if any(w in q for w in ["remediat", "action", "next step", "fix"]):
        return "remediation"
    return None