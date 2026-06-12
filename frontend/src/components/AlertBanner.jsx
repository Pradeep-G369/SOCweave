export default function AlertBanner({ verdict }) {
  if (!verdict) return null;

  const colorMap = {
    LOW: "bg-safe/10 border-safe text-safe",
    MEDIUM: "bg-progress/10 border-progress text-progress",
    HIGH: "bg-progress/10 border-progress text-progress",
    CRITICAL: "bg-threat/10 border-threat text-threat",
  };

  const iconMap = { LOW: "🟢", MEDIUM: "🟡", HIGH: "🟠", CRITICAL: "🔴" };

  const colorClass = colorMap[verdict.severity_after] || "bg-border text-textsecondary";
  const icon = iconMap[verdict.severity_after] || "⚪";

  const lines = verdict.summary.split("\n");

  return (
    <div
      role="alert"
      aria-live="polite"
      className={`border rounded-lg p-4 ${colorClass}`}
    >
      <p className="font-bold text-base">{icon} {lines[0]?.replace(icon + " ", "")}</p>
      <p className="text-textprimary text-sm mt-1">{lines[1]}</p>
      <p className="text-textsecondary text-sm mt-1">{lines[2]}</p>
    </div>
  );
}