import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Plus, FolderOpen } from "lucide-react";
import api from "../api/client";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = () => {
    api.get("/projects").then((res) => setProjects(res.data));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    await api.post("/projects", { name, description });
    setName("");
    setDescription("");
    setShowForm(false);
    loadProjects();
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-white">Projects</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-white px-4 py-2 rounded-lg transition"
        >
          <Plus size={18} />
          New Project
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-dark-800 border border-gray-700 rounded-xl p-6 mb-6"
        >
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-1">Project Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-1">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
              rows={3}
            />
          </div>
          <button
            type="submit"
            className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-2 rounded-lg transition"
          >
            Create
          </button>
        </form>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((p) => (
          <Link
            key={p.id}
            to={`/projects/${p.id}`}
            className="bg-dark-800 border border-gray-700 rounded-xl p-6 hover:border-emerald-500 transition"
          >
            <div className="flex items-center gap-3 mb-3">
              <FolderOpen className="text-emerald-400" size={20} />
              <h3 className="text-white font-semibold">{p.name}</h3>
            </div>
            <p className="text-gray-500 text-sm">{p.description || "No description"}</p>
            <p className="text-gray-600 text-xs mt-3">
              {new Date(p.created_at).toLocaleDateString()}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
