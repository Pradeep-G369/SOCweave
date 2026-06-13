import { useEffect, useState } from "react";

export default function ConfidenceBar({ confidence, severity }) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    setWidth(0);
    const timer = setTimeout(() => setWidth(confidence), 100);
    return () => clearTimeout(timer);
  }, [confidence]);

  // Color reflects severity outcome, not just confidence magnitude
  let colorClass = "bg-progress";
  if (severity === "LOW" || severity === "MEDIUM") colorClass = "bg-safe";
  else if (severity === "HIGH" || severity === "CRITICAL") colorClass = "bg-threat";

  return (
    <div className="mt-3">
      <div className="flex justify-between text-xs text-textsecondary mb-1">
        <span>Confidence Score</span>
        <span aria-live="polite">{confidence}%</span>
      </div>
      <div
        className="w-full h-3 bg-border rounded-full overflow-hidden"
        role="progressbar"
        aria-valuenow={confidence}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label="Confidence score"
      >
        <div
          className={`h-full ${colorClass} transition-all duration-1000 ease-out rounded-full`}
          style={{ width: `${width}%` }}
        />
      </div>
    </div>
  );
}