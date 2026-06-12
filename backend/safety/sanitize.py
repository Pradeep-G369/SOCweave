"""
Input sanitization: validates alert schema and applies basic rate-limit
tracking (in-memory, for demo purposes).
"""
import time

REQUIRED_FIELDS = ["alert_id", "severity", "title", "timestamp", "asset", "details"]
VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

# Simple in-memory rate limiter
_request_log: list[float] = []
RATE_LIMIT_PER_MIN = 10


def sanitize_alert(alert_data: dict) -> dict:
    """Validates required fields and severity enum. Raises ValueError if invalid."""
    _check_rate_limit()

    for field in REQUIRED_FIELDS:
        if field not in alert_data or not alert_data[field]:
            raise ValueError(f"Missing required field: {field}")

    if alert_data["severity"].upper() not in VALID_SEVERITIES:
        raise ValueError(f"Invalid severity: {alert_data['severity']}")

    # Normalize
    alert_data["severity"] = alert_data["severity"].upper()
    return alert_data


def _check_rate_limit():
    now = time.time()
    # Remove entries older than 60 seconds
    while _request_log and now - _request_log[0] > 60:
        _request_log.pop(0)

    if len(_request_log) >= RATE_LIMIT_PER_MIN:
        raise ValueError("Rate limit exceeded: max 10 requests per minute")

    _request_log.append(now)