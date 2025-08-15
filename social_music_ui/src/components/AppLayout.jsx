// src/components/AppLayout.jsx
import { NavLink, Link, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

/**
 * Layout oscuro/verde consistente para TODAS las pantallas protegidas
 * (Dashboard, Users, Instruments, Recordings, Samples).
 * Login y Signup se quedan como están (sin este layout).
 */
export default function AppLayout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-neutral-950 text-gray-100">
      {/* Header oscuro con acentos verdes */}
      <header className="border-b border-neutral-800 bg-neutral-900/60 backdrop-blur supports-[backdrop-filter]:bg-neutral-900/40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between py-3">
          {/* Logo + marca */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center shadow">
              <span className="text-white text-xl">🎵</span>
            </div>
            <h1 className="text-xl font-extrabold">
              <span className="text-white">Social</span>{" "}
              <span className="text-emerald-500">Music</span>
            </h1>
          </Link>

          {/* Nav */}
          <nav className="hidden md:flex items-center gap-1">
            <NavLink to="/" end className={({isActive}) => `px-3 py-2 rounded-md ${isActive ? 'text-white bg-neutral-800' : 'text-gray-300 hover:text-white'}`}>Inicio</NavLink>
            <NavLink to="/users" className={({isActive}) => `px-3 py-2 rounded-md ${isActive ? 'text-white bg-neutral-800' : 'text-gray-300 hover:text-white'}`}>Usuarios</NavLink>
            <NavLink to="/instruments" className={({isActive}) => `px-3 py-2 rounded-md ${isActive ? 'text-white bg-neutral-800' : 'text-gray-300 hover:text-white'}`}>Instrumentos</NavLink>
            <NavLink to="/recordings" className={({isActive}) => `px-3 py-2 rounded-md ${isActive ? 'text-white bg-neutral-800' : 'text-gray-300 hover:text-white'}`}>Grabaciones</NavLink>
            <NavLink to="/samples" className={({isActive}) => `px-3 py-2 rounded-md ${isActive ? 'text-white bg-neutral-800' : 'text-gray-300 hover:text-white'}`}>Samples</NavLink>
          </nav>

          {/* Usuario + logout */}
          <div className="flex items-center gap-3">
            {user?.email && (
              <span className="hidden sm:inline text-emerald-400">Hola {user.email}</span>
            )}
            <button onClick={logout} className="inline-flex items-center justify-center rounded-xl px-4 py-2 font-medium bg-red-600 hover:bg-red-500 text-white">
              Cerrar sesión
            </button>
          </div>
        </div>
      </header>

      {/* Contenido con tema oscuro */}
      <main className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
