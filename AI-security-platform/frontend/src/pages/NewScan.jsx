import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Crosshair } from "lucide-react";
import api from "../api/client";

export default function NewScan() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [targetUrl, setTargetUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await api.post(`/projects/${projectId}/scans`, {
        target_url: targetUrl,
      });
      navigate(`/projects/${projectId}/scans/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create scan");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold text-white mb-8">New Security Scan</h1>

      <form
        onSubmit={handleSubmit}
        className="bg-dark-800 border border-gray-700 rounded-xl p-8"
      >
        <div className="flex items-center gap-3 mb-6">
          <Crosshair className="text-emerald-400" size={24} />
          <p className="text-gray-400">
            Enter a target URL to scan for security vulnerabilities
          </p>
        </div>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <div className="mb-6">
          <label className="block text-gray-400 text-sm mb-1">Target URL</label>
          <input
            type="url"
            value={targetUrl}
            onChange={(e) => setTargetUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
            required
          />
        </div>

        <div className="bg-dark-900 border border-gray-700 rounded-lg p-4 mb-6">
          <p className="text-gray-400 text-sm font-medium mb-2">Scan Modules:</p>
          <div className="grid grid-cols-2 gap-2 text-sm text-gray-500">
            <span>Security Headers</span>
            <span>CORS Configuration</span>
            <span>Cookie Security</span>
            <span>HTTP Methods</span>
            <span>robots.txt Exposure</span>
            <span>Open Redirects</span>
            <span>Directory Listing</span>
            <span>Rate Limiting</span>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? "Creating scan..." : "Launch Scan"}
        </button>
      </form>
    </div>
  );
}
