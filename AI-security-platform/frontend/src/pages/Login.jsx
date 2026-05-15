import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Shield } from "lucide-react";
import useAuth from "../hooks/useAuth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/");
    } catch {
      setError("Invalid credentials");
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
          <h2 className="text-xl font-semibold text-white mb-6">Sign In</h2>

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
            Sign In
          </button>

          <p className="text-gray-500 text-sm mt-4 text-center">
            No account?{" "}
            <Link to="/register" className="text-emerald-400 hover:underline">
              Register
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
}
