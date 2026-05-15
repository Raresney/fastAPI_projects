import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Shield } from "lucide-react";
import useAuth from "../hooks/useAuth";

export default function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await register(email, username, password);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="flex items-center justify-center gap-2 mb-8">
          <Shield className="text-emerald-400" size={32} />
          <h1 className="text-2xl font-bold text-white">AI Security Platform</h1>
        </div>

        <form onSubmit={handleSubmit} className="bg-dark-800 rounded-xl p-8 border border-gray-700">
          <h2 className="text-xl font-semibold text-white mb-6">Create Account</h2>

          {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-1">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-gray-400 text-sm mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
              required
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-400 text-sm mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-dark-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-400"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-2 rounded-lg transition"
          >
            Create Account
          </button>

          <p className="text-gray-500 text-sm mt-4 text-center">
            Already have an account?{" "}
            <Link to="/login" className="text-emerald-400 hover:underline">
              Sign In
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
