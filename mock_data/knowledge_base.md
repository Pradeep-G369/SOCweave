# SOCweave Knowledge Base (Synthetic Threat Intelligence)

## CVE-2024-3094 — Supply Chain Backdoor
A backdoor injected into a compression library affecting SSH authentication.
Indicators: unexpected outbound connections, modified binary signatures on
build servers, beaconing to C2 infrastructure within hours of compromise.
Severity: CRITICAL. Recommended action: isolate host, rotate SSH keys,
audit recent package builds.

## MITRE ATT&CK T1041 — Exfiltration Over C2 Channel
Adversaries steal data by sending it over an existing command-and-control
channel. Indicators: large outbound transfers to non-business-hours
destinations, connections to known-bad IP reputation lists, transfer
volume inconsistent with normal business traffic.

## Policy: Scheduled Maintenance Windows
Internal IT policy requires all bulk file operations (deletion, archival,
compression >1GB) to have an approved IT helpdesk ticket AND a notification
email to the security distribution list at least 12 hours in advance.
Operations matching both signals should be treated as authorized.

## Policy: Outbound Transfer Authorization
Any outbound transfer exceeding 500MB to an external IP must have a
corresponding change-request ticket. Absence of a ticket combined with
threat-intel IP matches should be treated as high-confidence malicious.