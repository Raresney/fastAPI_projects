const colors = {
  critical: "bg-red-600 text-white",
  high: "bg-orange-500 text-white",
  medium: "bg-yellow-500 text-dark-900",
  low: "bg-blue-500 text-white",
  info: "bg-gray-500 text-white",
};

export default function SeverityBadge({ severity }) {
  return (
    <span
      className={`px-2 py-0.5 rounded text-xs font-semibold uppercase ${colors[severity] || colors.info}`}
    >
      {severity}
    </span>
  );
}
