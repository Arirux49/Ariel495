import { Navigate, useLocation, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-2xl text-white">🌀</span>
          </div>
          <p>Cargando...</p>
        </div>
      </div>
    );
  }

  const authed =
    typeof isAuthenticated === "function" ? isAuthenticated() : !!isAuthenticated;

  if (!authed) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // ✅ Soporta ambos patrones: children o Outlet
  return children ?? <Outlet />;
};

export default ProtectedRoute;