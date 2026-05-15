import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Plus, Scan } from "lucide-react";
import api from "../api/client";
import SeverityBadge from "../components/SeverityBadge";

const statusColors = {
  pending: "text-gray-400",
  running: "text-blue-400",
  completed: "text-emerald-400",
  failed: "text-red-400",
};

export default function ProjectDetail() {
  const { projectId } = useParams();
  const [project, setProject] = useState(null);
  const [scans, setScans] = useState([]);

  useEffect(() => {
    api.get(`/projects/${projectId}`).then((res) => setProject(res.data));
    api.get(`/projects/${projectId}/scans`).then((res) => setScans(res.data));
  }, [projectId]);

  if (!project) return null;

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">{project.name}</h1>
          <p className="text-gray-500 mt-1">{project.description}</p>
        </div>
        <Link
          to={`/projects/${projectId}/scan`}
          className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition"
        >
          <Plus size={18} />
          New Scan
        </Link>
      </div>

      <div className="bg-dark-800 border border-gray-700 rounded-xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="text-left text-gray-400 text-sm px-6 py-3">Target</th>
              <th className="text-left text-gray-400 text-sm px-6 py-3">Status</th>
              <th className="text-left text-gray-400 text-sm px-6 py-3">Date</th>
              <th className="text-right text-gray-400 text-sm px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {scans.map((s) => (
              <tr key={s.id} className="border-b border-gray-700/50 hover:bg-dark-700/30">
                <td className="px-6 py-4 text-white text-sm">{s.target_url}</td>
                <td className="px-6 py-4">
                  <span className={`text-sm font-medium ${statusColors[s.status]}`}>
                    {s.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-gray-500 text-sm">
                  {new Date(s.created_at).toLocaleString()}
                </td>
                <td className="px-6 py-4 text-right">
                  <Link
                    to={`/projects/${projectId}/scans/${s.id}`}
                    className="text-emerald-400 hover:underline text-sm"
                  >
                    View
                  </Link>
                </td>
              </tr>
            ))}
            {scans.length === 0 && (
              <tr>
                <td colSpan={4} className="text-center py-12 text-gray-500">
                  <Scan className="mx-auto mb-3" size={32} />
                  No scans yet — create your first scan
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
