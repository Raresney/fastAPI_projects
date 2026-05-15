import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Play, FileText } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import api from "../api/client";
import useWebSocket from "../hooks/useWebSocket";
import SeverityBadge from "../components/SeverityBadge";
import ScanLogStream from "../components/ScanLogStream";

const SEVERITY_COLORS = {
  critical: "#dc2626",
  high: "#f97316",
  medium: "#eab308",
  low: "#3b82f6",
  info: "#6b7280",
};

export default function ScanDetail() {
  const { projectId, scanId } = useParams();
  const [scan, setScan] = useState(null);
  const [findings, setFindings] = useState([]);
  const [running, setRunning] = useState(false);
  const { logs } = useWebSocket(scanId);

  useEffect(() => {
    loadScan();
  }, [scanId]);

  const loadScan = () => {
    api.get(`/projects/${projectId}/scans/${scanId}`).then((res) => setScan(res.data));
    api.get(`/projects/${projectId}/scans/${scanId}/findings`).then((res) => setFindings(res.data));
  };

  const runScan = async () => {
    setRunning(true);
    try {
      await api.post(`/projects/${projectId}/scans/${scanId}/run`);
      loadScan();
    } finally {
      setRunning(false);
    }
  };

  if (!scan) return null;

  const severityCounts = findings.reduce((acc, f) => {
    acc[f.severity] = (acc[f.severity] || 0) + 1;
    return acc;
  }, {});

  const chartData = Object.entries(severityCounts).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">Scan Results</h1>
          <p className="text-gray-500 mt-1">{scan.target_url}</p>
        </div>
        <div className="flex gap-3">
          {scan.status === "pending" && (
            <button
              onClick={runScan}
              disabled={running}
              className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg transition"
            >
              <Play size={18} />
              {running ? "Running..." : "Run Scan"}
            </button>
          )}
          {findings.length > 0 && (
            <Link
              to={`/projects/${projectId}/scans/${scanId}/report`}
              className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
            >
              <FileText size={18} />
              AI Report
            </Link>
          )}
        </div>
      </div>

      {(running || logs.length > 0) && (
        <div className="mb-6">
          <h2 className="text-lg font-semibold text-white mb-3">Live Scan Logs</h2>
          <ScanLogStream logs={logs} />
        </div>
      )}

      {chartData.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Severity Distribution</h2>
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80}>
                  {chartData.map((entry) => (
                    <Cell key={entry.name} fill={SEVERITY_COLORS[entry.name]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Summary</h2>
            <div className="space-y-3">
              {Object.entries(severityCounts).map(([sev, count]) => (
                <div key={sev} className="flex items-center justify-between">
                  <SeverityBadge severity={sev} />
                  <span className="text-white font-semibold">{count}</span>
                </div>
              ))}
              <div className="border-t border-gray-700 pt-3 flex justify-between">
                <span className="text-gray-400">Total</span>
                <span className="text-white font-bold">{findings.length}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="bg-dark-800 border border-gray-700 rounded-xl overflow-hidden">
        <h2 className="text-lg font-semibold text-white px-6 py-4 border-b border-gray-700">
          Findings ({findings.length})
        </h2>
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="text-left text-gray-400 text-sm px-6 py-3">Severity</th>
              <th className="text-left text-gray-400 text-sm px-6 py-3">Title</th>
              <th className="text-left text-gray-400 text-sm px-6 py-3">Category</th>
            </tr>
          </thead>
          <tbody>
            {findings.map((f) => (
              <tr key={f.id} className="border-b border-gray-700/50">
                <td className="px-6 py-3">
                  <SeverityBadge severity={f.severity} />
                </td>
                <td className="px-6 py-3">
                  <p className="text-white text-sm">{f.title}</p>
                  <p className="text-gray-500 text-xs mt-1">{f.description}</p>
                </td>
                <td className="px-6 py-3 text-gray-400 text-sm">{f.category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
