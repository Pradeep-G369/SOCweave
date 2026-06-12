export default function VerdictCard({ verdict }) {
  if (!verdict) return null;

  const deltaIcon = { up: "⬆️", down: "⬇️", flat: "➡️" }[verdict.delta_direction] || "➡️";
  const deltaColor = { up: "text-threat", down: "text-safe", flat: "text-textsecondary" }[verdict.delta_direction];

  return (
    <div className="border border-border rounded-lg p-4 mt-4">
      <h3 className="font-bold text-sm mb-2">⚖️ Final Verdict</h3>
      <p className={`text-sm font-semibold ${deltaColor}`}>{deltaIcon} {verdict.delta_label}</p>
      <p className="text-sm mt-2"><strong>Status:</strong> {verdict.status}</p>
      <p className="text-sm"><strong>Evidence:</strong> Based on {verdict.evidence_count} cited sources across 3 IQ agents</p>

      {verdict.critic_notes && verdict.critic_notes.length > 0 && (
        <div className="mt-2 p-2 bg-progress/10 border border-progress rounded text-xs text-progress">
          <strong>🔁 Critic Loop:</strong>
          <ul className="list-disc ml-4 mt-1">
            {verdict.critic_notes.map((n, i) => <li key={i}>{n}</li>)}
          </ul>
        </div>
      )}

      {verdict.remediation && verdict.remediation.length > 0 && (
        <div className="mt-3">
          <p className="font-semibold text-sm mb-1">🛠️ Remediation Plan:</p>
          <ul className="list-disc ml-5 text-sm text-textsecondary">
            {verdict.remediation.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}