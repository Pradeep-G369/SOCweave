export default function AnalystReasoning({ verdict }) {
  if (!verdict || !verdict.reasoning_chain) return null;

  return (
    <div className="border border-border rounded-lg p-4 mt-4 bg-canvas">
      <h3 className="font-bold text-sm mb-2 text-textprimary">🧑‍💻 Analyst Reasoning</h3>
      <p className="text-sm text-textsecondary leading-relaxed">
        {verdict.reasoning_chain}
      </p>
    </div>
  );
}