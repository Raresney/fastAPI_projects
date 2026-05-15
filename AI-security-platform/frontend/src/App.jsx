import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import ProjectDetail from "./pages/ProjectDetail";
import NewScan from "./pages/NewScan";
import ScanDetail from "./pages/ScanDetail";
import Report from "./pages/Report";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:projectId" element={<ProjectDetail />} />
          <Route path="/projects/:projectId/scan" element={<NewScan />} />
          <Route path="/projects/:projectId/scans/:scanId" element={<ScanDetail />} />
          <Route path="/projects/:projectId/scans/:scanId/report" element={<Report />} />
        </Route>
      </Route>
    </Routes>
  );
}
