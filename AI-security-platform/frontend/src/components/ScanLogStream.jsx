import { useEffect, useRef } from "react";

const levelColors = {
  info: "text-blue-400",
  warning: "text-yellow-400",
  error: "text-red-400",
  finding: "text-emerald-400",
  scan_started: "text-cyan-400",
  scan_completed: "text-green-400",
};

export default function ScanLogStream({ logs }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="bg-dark-900 border border-gray-700 rounded-lg p-4 h-80 overflow-y-auto font-mono text-sm">
      {logs.length === 0 && (
        <p className="text-gray-500">Waiting for scan logs...</p>
      )}
      {logs.map((log, i) => (
        <div key={i} className="flex gap-2 py-0.5">
          <span className={levelColors[log.type] || "text-gray-400"}>
            [{log.type}]
          </span>
          <span className="text-gray-300">
            {log.message || log.title || JSON.stringify(log)}
          </span>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
