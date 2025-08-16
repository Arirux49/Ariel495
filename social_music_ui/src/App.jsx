import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// ...resto de imports

export default function App() {
  return (
    // 👇 sin la barra final (esto a veces importa para el match)
    <BrowserRouter basename="/Ariel495">
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

          {/* Catch-all por si algo no matchea */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

