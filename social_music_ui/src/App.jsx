// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// ...tus imports

export default function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <AuthProvider>
        <Routes>
          {/* Públicas */}
          <Route element={<PublicRoute />}>
            <Route path="/login" element={<LoginScreen />} />
            <Route path="/signup" element={<SignupScreen />} />
          </Route>

          {/* Protegidas */}
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

          {/* Catch-all (opcional, ayuda si algo no matchea) */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
