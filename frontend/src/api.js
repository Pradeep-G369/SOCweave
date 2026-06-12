const API_BASE = "http://127.0.0.1:8000";

export async function fetchScenario(name) {
  const res = await fetch(`${API_BASE}/scenario/${name}`);
  if (!res.ok) throw new Error(`Failed to fetch scenario ${name}`);
  return res.json();
}