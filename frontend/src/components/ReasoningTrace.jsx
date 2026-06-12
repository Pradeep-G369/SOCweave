export default function ReasoningTrace({ plan, auditTrail }) {
  if (!plan) return null;

  return (
    <div className="border border-border rounded-lg p-4 bg-canvas">
      <h3 className="font-bold text-sm mb-2 text-textprimary">🧭 Reasoning Plan</h3>
      <ol className="space-y-1 text-sm">
        {plan.map((step, i) => {
          const done = auditTrail && auditTrail[i];
          return (
            <li key={i} className="flex items-center gap-2">
              <span className={done ? "text-safe" : "text-textsecondary"}>
                {done ? "✅" : "⏳"}
              </span>
              <span className={done ? "text-textprimary" : "text-textsecondary"}>
                {step}
              </span>
              {done && (
                <span className="text-xs text-textsecondary ml-auto">
                  {done.elapsed_seconds}s
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </div>
  );
}