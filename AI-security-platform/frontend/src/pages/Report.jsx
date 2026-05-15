import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FileText, Loader } from "lucide-react";
import api from "../api/client";

export default function Report() {
  const { projectId, scanId } = useParams();
  const [reports, setReports] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [reportType, setReportType] = useState("executive");

  useEffect(() => {
    loadReports();
  }, [scanId]);

  const loadReports = () => {
    api
      .get(`/projects/${projectId}/scans/${scanId}/reports`)
      .then((res) => setReports(res.data));
  };

  const generateReport = async () => {
    setGenerating(true);
    try {
      await api.post(`/projects/${projectId}/scans/${scanId}/reports`, {
        report_type: reportType,
      });
      loadReports();
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-8">AI Reports</h1>

      <div className="bg-dark-800 border border-gray-700 rounded-xl p-6 mb-8">
        <h2 className="text-lg font-semibold text-white mb-4">Generate New Report</h2>
        <div className="flex gap-4 items-end">
          <div>
            <label className="block text-gray-400 text-sm mb-1">Report Type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
            >
              <option value="executive">Executive Summary</option>
              <option value="technical">Technical Report</option>
            </select>
          </div>
          <button
            onClick={generateReport}
            disabled={generating}
            className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
          >
            {generating ? <Loader className="animate-spin" size={18} /> : <FileText size={18} />}
            {generating ? "Generating..." : "Generate"}
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {reports.map((r) => (
          <div key={r.id} className="bg-dark-800 border border-gray-700 rounded-xl p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-white font-semibold capitalize">{r.report_type} Report</h3>
              <span className="text-gray-500 text-sm">
                {new Date(r.created_at).toLocaleString()}
              </span>
            </div>

            {r.ai_summary && (
              <div className="bg-dark-900 border border-gray-700 rounded-lg p-4 mb-4">
                <p className="text-gray-400 text-sm font-medium mb-2">AI Summary</p>
                <p className="text-gray-300 text-sm leading-relaxed">{r.ai_summary}</p>
              </div>
            )}

            {r.content && (
              <div className="bg-dark-900 border border-gray-700 rounded-lg p-4">
                <p className="text-gray-400 text-sm font-medium mb-2">Report Data</p>
                <pre className="text-gray-300 text-xs overflow-x-auto whitespace-pre-wrap">
                  {JSON.stringify(r.content, null, 2)}
                </pre>
              </div>
            )}
          </div>
        ))}

        {reports.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            <FileText className="mx-auto mb-3" size={40} />
            <p>No reports generated yet</p>
          </div>
        )}
      </div>
    </div>
  );
}
