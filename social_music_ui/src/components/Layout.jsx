// src/components/Layout.jsx
import { NavLink, Link, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Light layout by default. If the current route starts with /instruments,
 * we wrap the Outlet with a .theme-dark container so only that section is dark.
 */
export default function Layout() {
  const { user, logout } = useAuth();
  const { pathname } = useLocation();
  const isInstruments = pathname.startsWith("/instruments");

  const content = (
    <div className={isInstruments ? "theme-dark min-h-screen" : "min-h-screen"}>
      <main className="py-8">
        <div className="container-page">
          <Outlet />
        </div>
      </main>
    </div>
  );

  return (
    <div className="min-h-screen">
      {/* Light Header */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="container-page flex items-center justify-between py-3">
          {/* Logo + brand */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center shadow">
              <span className="text-white text-xl">🎵</span>
            </div>
            <h1 className="text-xl font-extrabold">
              <span className="text-gray-900">Social</span>{" "}
              <span className="text-emerald-600">Music</span>
            </h1>
          </Link>

          {/* Nav */}
          <nav className="hidden md:flex items-center gap-1">
            <NavLink to="/" end className={({isActive}) => `nav-link ${isActive ? 'nav-link-active' : ''}`}>Inicio</NavLink>
            <NavLink to="/users" className={({isActive}) => `nav-link ${isActive ? 'nav-link-active' : ''}`}>Usuarios</NavLink>
            <NavLink to="/instruments" className={({isActive}) => `nav-link ${isActive ? 'nav-link-active' : ''}`}>Instrumentos</NavLink>
            <NavLink to="/recordings" className={({isActive}) => `nav-link ${isActive ? 'nav-link-active' : ''}`}>Grabaciones</NavLink>
            <NavLink to="/samples" className={({isActive}) => `nav-link ${isActive ? 'nav-link-active' : ''}`}>Samples</NavLink>
          </nav>

          {/* User + logout */}
          <div className="flex items-center gap-3">
            {user?.email && (
              <span className="hidden sm:inline text-emerald-700">Hola {user.email}</span>
            )}
            <button onClick={logout} className="btn-green">Cerrar sesión</button>
          </div>
        </div>
      </header>

      {content}
    </div>
  );
}
