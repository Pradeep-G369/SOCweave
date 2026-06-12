"""
Work IQ Agent — Human/organizational context plane.
Simulates Work IQ: scans M365 emails, Teams messages, and IT tickets to
find (or rule out) human authorization for the observed activity.
"""
import time


def run(alert_data: dict) -> dict:
    start = time.time()
    work = alert_data.get("work_iq", {})

    tickets = work.get("tickets", [])
    emails = work.get("emails", [])
    citations = work.get("citations", [])

    findings = []
    # Reasoning: presence of approved tickets/emails = authorization signal
    authorization_signal = 0  # 0 = no authorization found, 100 = fully authorized

    if tickets:
        for t in tickets:
            findings.append(f"IT Ticket {t['id']}: \"{t['title']}\" (status: {t['status']})")
            if t.get("status", "").lower() == "approved":
                authorization_signal += 50

    if emails:
        for e in emails:
            findings.append(f"Email from {e['from']} ({e['time']}): \"{e['subject']}\"")
            authorization_signal += 45

    if not tickets and not emails:
        findings.append("No IT tickets or emails found referencing this asset/activity")
        authorization_signal = 0

    authorization_signal = min(authorization_signal, 100)

    elapsed = round(time.time() - start, 2)

    return {
        "agent": "Work IQ Agent",
        "role": "Human Context & Authorization Check",
        "findings": findings,
        "citations": citations,
        "authorization_signal": authorization_signal,  # 0-100
        "elapsed_seconds": elapsed,
    }