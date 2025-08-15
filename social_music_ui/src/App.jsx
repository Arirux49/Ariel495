// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import PublicRoute from "./components/PublicRoute";
import ProtectedRoute from "./components/ProtectedRoute";

// Pantallas
import LoginScreen from "./components/LoginScreen";
import SignupScreen from "./components/SignupScreen";
import Dashboard from "./components/Dashboard";
import UsersPage from "./components/UsersPage";
import InstrumentsPage from "./components/InstrumentsPage";
import RecordingsPage from "./components/RecordingsPage";
import SamplesPage from "./components/SamplesPage";
import SampleDetail from "./components/SampleDetail";

// Nuevo layout oscuro para pantallas protegidas
import AppLayout from "./components/AppLayout";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Públicas: se mantienen tal cual */}
          <Route element={<PublicRoute />}>
            <Route path="/login" element={<LoginScreen />} />
            <Route path="/signup" element={<SignupScreen />} />
          </Route>

          {/* Protegidas: todas con AppLayout oscuro/verde */}
          <Route element={<ProtectedRoute />}>
            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/instruments" element={<InstrumentsPage />} />
              <Route path="/recordings" element={<RecordingsPage />} />
              <Route path="/samples" element={<SamplesPage />} />
              <Route path="/samples/:id" element={<SampleDetail />} />
            </Route>
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
