import { useState } from "react";

function AgentBlock({ data }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="border border-border rounded-md mb-2">
      <button
        onClick={() => setOpen(!open)}
        aria-expanded={open}
        className="w-full text-left p-3 flex justify-between items-center text-sm font-medium hover:bg-border/40"
      >
        <span>{open ? "▼" : "▶"} {data.agent} — {data.role}</span>
        <span className="text-xs text-textsecondary">{data.elapsed_seconds}s</span>
      </button>
      {open && (
        <div className="p-3 pt-0 text-sm text-textsecondary">
          <ul className="list-disc ml-5 mb-2">
            {data.findings.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
          <p className="font-semibold text-textprimary mt-2 mb-1">Citations:</p>
          <ul className="list-disc ml-5 text-citelink text-xs">
            {data.citations.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function AuditTrail({ agents }) {
  if (!agents) return null;
  return (
    <div className="mt-4">
      <h3 className="font-bold text-sm mb-2">📋 Agent Audit Trail</h3>
      <AgentBlock data={agents.foundry_iq} />
      <AgentBlock data={agents.fabric_iq} />
      <AgentBlock data={agents.work_iq} />
    </div>
  );
}