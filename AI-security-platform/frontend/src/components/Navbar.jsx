import { Link, useNavigate } from "react-router-dom";
import { Shield, LogOut } from "lucide-react";
import useAuth from "../hooks/useAuth";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="bg-dark-800 border-b border-gray-700">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link to="/" className="flex items-center gap-2 text-emerald-400 font-bold text-lg">
          <Shield size={24} />
          AI Security Platform
        </Link>

        <div className="flex items-center gap-6">
          <Link to="/" className="text-gray-300 hover:text-white transition">
            Dashboard
          </Link>
          <Link to="/projects" className="text-gray-300 hover:text-white transition">
            Projects
          </Link>
          <span className="text-gray-500 text-sm">{user?.username}</span>
          <button
            onClick={handleLogout}
            className="text-gray-400 hover:text-red-400 transition"
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </nav>
  );
}
