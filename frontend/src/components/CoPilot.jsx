import { useState } from "react";

const SUGGESTIONS = [
  "Why was this verdict reached?",
  "What evidence supports this?",
  "What are the next steps?",
];

export default function CoPilot({ result }) {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const ask = async (text) => {
    const q = text || question;
    if (!q.trim()) return;
    setChat((c) => [...c, { role: "user", text: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q, context: result }),
      });
      const data = await res.json();
      setChat((c) => [...c, { role: "assistant", text: data.answer }]);
    } catch {
      setChat((c) => [...c, { role: "assistant", text: "Error reaching co-pilot — is the backend running?" }]);
    } finally {
      setLoading(false);
    }
  };

  if (!result) return null;

  return (
    <div className="border border-border rounded-lg p-4 mt-4">
      <h3 className="font-bold text-sm mb-2">💬 Analyst Co-Pilot</h3>

      {chat.length === 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {SUGGESTIONS.map((s, i) => (
            <button
              key={i}
              onClick={() => ask(s)}
              className="text-xs px-2 py-1 border border-border rounded-full text-textsecondary hover:text-textprimary hover:border-citelink"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      <div className="space-y-2 mb-3 max-h-48 overflow-y-auto" aria-live="polite">
        {chat.map((m, i) => (
          <div key={i} className={`text-sm ${m.role === "user" ? "text-textprimary" : "text-citelink"}`}>
            <strong>{m.role === "user" ? "You: " : "Co-Pilot: "}</strong>{m.text}
          </div>
        ))}
        {loading && <div className="text-sm text-textsecondary">Co-Pilot is thinking...</div>}
      </div>

      <div className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && ask()}
          placeholder="Ask about this verdict..."
          aria-label="Ask the analyst co-pilot a question"
          className="flex-1 bg-canvas border border-border rounded px-3 py-2 text-sm text-textprimary"
        />
        <button
          onClick={() => ask()}
          disabled={loading}
          className="px-3 py-2 bg-citelink text-white rounded text-sm disabled:opacity-50"
        >
          Ask
        </button>
      </div>
    </div>
  );
}