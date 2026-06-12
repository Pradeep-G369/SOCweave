import { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({ startOnLoad: false, theme: "dark" });

export default function BlastRadiusMap({ graph, asset }) {
  const ref = useRef(null);

  useEffect(() => {
    if (!graph || !ref.current) return;

    const nodeLines = graph.nodes
      .map((n) => `  ${n.replace(/[^a-zA-Z0-9]/g, "_")}["${n}"]`)
      .join("\n");

    const edgeLines = graph.edges
      .map(([a, b]) => `  ${a.replace(/[^a-zA-Z0-9]/g, "_")} --> ${b.replace(/[^a-zA-Z0-9]/g, "_")}`)
      .join("\n");

    const definition = `graph TD\n${nodeLines}\n${edgeLines}`;

    mermaid.render(`blast-${asset}-${Date.now()}`, definition).then(({ svg }) => {
      if (ref.current) ref.current.innerHTML = svg;
    }).catch(() => {
      if (ref.current) ref.current.innerHTML = "<p class='text-textsecondary text-sm'>Diagram unavailable</p>";
    });
  }, [graph, asset]);

  return (
    <div className="border border-border rounded-lg p-4 mt-4">
      <h3 className="font-bold text-sm mb-2">🗺️ Blast Radius Map</h3>
      <div ref={ref} aria-label="Blast radius diagram" role="img" />
    </div>
  );
}