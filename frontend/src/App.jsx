import { useState, useRef } from "react";
import { fetchScenario } from "./api";
import AlertBanner from "./components/AlertBanner";
import ConfidenceBar from "./components/ConfidenceBar";
import ReasoningTrace from "./components/ReasoningTrace";
import AuditTrail from "./components/AuditTrail";
import BlastRadiusMap from "./components/BlastRadiusMap";
import VerdictCard from "./components/VerdictCard";
import AnalystReasoning from "./components/AnalystReasoning";
import CoPilot from "./components/CoPilot";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stopwatch, setStopwatch] = useState(0);
  const [activeScenario, setActiveScenario] = useState(null);
  const intervalRef = useRef(null);

  const runScenario = async (name) => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    setLoading(true);
    setResult(null);
    setActiveScenario(name);
    setStopwatch(0);

    const startTime = Date.now();
    intervalRef.current = setInterval(() => {
      setStopwatch(((Date.now() - startTime) / 1000).toFixed(1));
    }, 100);

    try {
      const data = await fetchScenario(name);
      const elapsed = Date.now() - startTime;
      if (elapsed < 1000) {
        await new Promise((resolve) => setTimeout(resolve, 1000 - elapsed));
      }
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      clearInterval(intervalRef.current);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-canvas text-textprimary p-6 max-w-4xl mx-auto">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">🛡️ SOCweave</h1>
        <p className="text-textsecondary text-sm mt-1">
          Weaving threat intelligence, infrastructure data, and human context
          into one resolved verdict. Every time. Under 60 seconds.
        </p>
      </header>

      <div className="flex gap-3 mb-6 flex-wrap">
        <button
          onClick={() => runScenario("a")}
          disabled={loading}
          aria-label="Run Scenario A: False Positive Alert"
          className="px-4 py-2 bg-citelink text-white rounded-md text-sm font-medium hover:opacity-90 disabled:opacity-50"
        >
          ▶ Run Scenario A (False Positive)
        </button>
        <button
          onClick={() => runScenario("b")}
          disabled={loading}
          aria-label="Run Scenario B: Real Threat Alert"
          className="px-4 py-2 bg-threat text-white rounded-md text-sm font-medium hover:opacity-90 disabled:opacity-50"
        >
          ▶ Run Scenario B (Real Threat)
        </button>
        <button
          onClick={() => runScenario("c")}
          disabled={loading}
          aria-label="Run Scenario C: Ambiguous Insider Activity"
          className="px-4 py-2 bg-progress text-white rounded-md text-sm font-medium hover:opacity-90 disabled:opacity-50"
        >
          ▶ Run Scenario C (Ambiguous Activity)
        </button>

        <div
          className="ml-auto flex items-center gap-2 px-3 py-2 border border-border rounded-md text-sm font-mono"
          aria-live="polite"
        >
          ⏱️ {stopwatch}s
        </div>
      </div>

      {loading && (
        <div className="text-center text-textsecondary py-8" role="status">
          Running multi-agent pipeline...
        </div>
      )}

      {result && !loading && (
        <div className="space-y-4">
          <div className="text-xs text-textsecondary">
            Alert: <strong>{result.verdict.alert_id}</strong> | Asset:{" "}
            <strong>{result.verdict.asset}</strong> | Total reasoning time:{" "}
            <strong>{result.total_elapsed_seconds}s</strong>
          </div>
          <AlertBanner verdict={result.verdict} />
          <AnalystReasoning verdict={result.verdict} />
          <ConfidenceBar confidence={result.verdict.confidence} severity={result.verdict.severity_after} />
          <ReasoningTrace plan={result.plan} auditTrail={result.audit_trail} />
          <AuditTrail agents={result.agents} />
          <BlastRadiusMap graph={result.agents.fabric_iq.graph} asset={result.verdict.asset} />
          <VerdictCard verdict={result.verdict} />
          <CoPilot result={result} />
        </div>
      )}

      {!result && !loading && (
        <div className="text-center text-textsecondary py-12 border border-dashed border-border rounded-lg">
          Click a scenario above to see SOCweave's multi-agent reasoning in action.
        </div>
      )}

      <footer className="mt-8 text-xs text-textsecondary text-center">
        Built for Microsoft Agents League 2026 — Reasoning Agents Track | WCAG 2.1 AA Accessible
      </footer>
    </div>
  );
}