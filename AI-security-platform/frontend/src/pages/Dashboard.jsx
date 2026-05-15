import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FolderOpen, Scan, AlertTriangle, Shield } from "lucide-react";
import api from "../api/client";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [stats, setStats] = useState({ projects: 0, scans: 0, findings: 0 });

  useEffect(() => {
    api.get("/projects").then((res) => {
      setProjects(res.data);
      setStats((s) => ({ ...s, projects: res.data.length }));
    });
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold text-white mb-8">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <FolderOpen className="text-emerald-400" size={20} />
            <span className="text-gray-400">Projects</span>
          </div>
          <p className="text-3xl font-bold text-white">{stats.projects}</p>
        </div>

        <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <Scan className="text-blue-400" size={20} />
            <span className="text-gray-400">Total Scans</span>
          </div>
          <p className="text-3xl font-bold text-white">{stats.scans}</p>
        </div>

        <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-2">
            <AlertTriangle className="text-yellow-400" size={20} />
            <span className="text-gray-400">Findings</span>
          </div>
          <p className="text-3xl font-bold text-white">{stats.findings}</p>
        </div>
      </div>

      <div className="bg-dark-800 border border-gray-700 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white">Recent Projects</h2>
          <Link
            to="/projects"
            className="text-emerald-400 hover:underline text-sm"
          >
            View all
          </Link>
        </div>

        {projects.length === 0 ? (
          <div className="text-center py-12">
            <Shield className="mx-auto text-gray-600 mb-3" size={40} />
            <p className="text-gray-500">No projects yet</p>
            <Link
              to="/projects"
              className="text-emerald-400 hover:underline text-sm mt-2 inline-block"
            >
              Create your first project
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {projects.slice(0, 5).map((p) => (
              <Link
                key={p.id}
                to={`/projects/${p.id}`}
                className="block bg-dark-900 border border-gray-700 rounded-lg p-4 hover:border-emerald-500 transition"
              >
                <h3 className="text-white font-medium">{p.name}</h3>
                <p className="text-gray-500 text-sm mt-1">
                  {p.description || "No description"}
                </p>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
