"""
PII Scrubbing — uses Microsoft Presidio to detect and redact personal
information (names, emails, phone numbers, IPs) from human-context data
(Work IQ emails/tickets) before it's processed by any agent.
"""
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    _analyzer = AnalyzerEngine()
    _anonymizer = AnonymizerEngine()
    _PRESIDIO_AVAILABLE = True
except Exception:
    _PRESIDIO_AVAILABLE = False


ENTITIES_TO_SCRUB = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "IP_ADDRESS"]


def _scrub_text(text: str) -> str:
    if not _PRESIDIO_AVAILABLE or not text:
        return text
    try:
        results = _analyzer.analyze(text=text, entities=ENTITIES_TO_SCRUB, language="en")
        anonymized = _anonymizer.anonymize(text=text, analyzer_results=results)
        return anonymized.text
    except Exception:
        return text


def scrub_pii(alert_data: dict) -> dict:
    """Scrubs PII from work_iq emails/tickets in-place. Keeps technical
    fields (asset names, IPs in foundry_iq/fabric_iq) untouched since those
    are needed for security analysis - only human-context text is scrubbed."""
    work = alert_data.get("work_iq", {})

    for email in work.get("emails", []):
        email["body"] = _scrub_text(email.get("body", ""))
        # Keep sender name as a role label only (already synthetic in our demo)

    for ticket in work.get("tickets", []):
        ticket["title"] = _scrub_text(ticket.get("title", ""))

    return alert_data