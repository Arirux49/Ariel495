import { useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const navItems = [
  { to: "/dashboard", label: "Inicio" },
  { to: "/users", label: "Usuarios" },
  { to: "/instruments", label: "Instrumentos" },
  { to: "/recordings", label: "Grabaciones" },
  { to: "/samples", label: "Samples" },
];

export default function AppShell({ children, title = "Social Music" }) {
  const [open, setOpen] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-zinc-900 to-black text-zinc-100">
      <header className="sticky top-0 z-40 backdrop-blur bg-black/40 border-b border-zinc-800">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              className="md:hidden inline-flex items-center justify-center rounded-xl border border-zinc-800 p-2 hover:bg-zinc-900 transition"
              onClick={() => setOpen(true)}
              aria-label="Abrir menú"
            >
              ☰
            </button>
            <Link to="/dashboard" className="flex items-center gap-2">
              <span className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500 text-black font-bold shadow-lg">
                ♪
              </span>
              <span className="font-semibold tracking-tight">Social Music</span>
            </Link>
          </div>

          <nav className="hidden md:flex items-center gap-1">
            {navItems.map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  [
                    "rounded-xl px-3 py-2 text-sm font-medium transition",
                    isActive
                      ? "bg-emerald-500 text-black"
                      : "text-zinc-300 hover:text-white hover:bg-zinc-900",
                  ].join(" ")
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            <div className="hidden sm:flex flex-col leading-tight text-right">
              <span className="text-sm text-zinc-300">Hola</span>
              <span className="text-emerald-400 font-medium truncate max-w-[200px]">
                {user?.email}
              </span>
            </div>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-500 text-black px-3 py-2 font-medium hover:bg-emerald-400 active:scale-[0.99] transition shadow-lg"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </header>

      {open && (
        <div className="fixed inset-0 z-50 md:hidden">
          <div className="absolute inset-0 bg-black/60" onClick={() => setOpen(false)} />
          <div className="absolute left-0 top-0 h-full w-80 bg-zinc-950 border-r border-zinc-800 p-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <span className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-500 text-black font-bold shadow-lg">
                  ♪
                </span>
                <span className="font-semibold">Social Music</span>
              </div>
              <button
                className="rounded-xl border border-zinc-800 p-2 hover:bg-zinc-900 transition"
                onClick={() => setOpen(false)}
                aria-label="Cerrar menú"
              >
                ✕
              </button>
            </div>
            <nav className="space-y-1">
              {navItems.map(({ to, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  onClick={() => setOpen(false)}
                  className={({ isActive }) =>
                    [
                      "flex items-center gap-3 rounded-xl px-3 py-2 transition",
                      isActive
                        ? "bg-emerald-500 text-black font-semibold"
                        : "hover:bg-zinc-900 text-zinc-300 hover:text-white",
                    ].join(" ")
                  }
                >
                  {label}
                </NavLink>
              ))}
            </nav>
            <div className="mt-6 pt-4 border-t border-zinc-800">
              <button
                onClick={() => { setOpen(false); handleLogout(); }}
                className="w-full inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-500 text-black px-3 py-2 font-semibold hover:bg-emerald-400 active:scale-[0.99] transition shadow-lg"
              >
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="mb-4">
          <h1 className="text-2xl md:text-3xl font-bold tracking-tight">{title}</h1>
          <p className="text-zinc-400 text-sm">Gestiona tu música con estilo verde/negro.</p>
        </div>
        <div className="bg-zinc-950/60 border border-zinc-800 rounded-2xl p-4 md:p-6 shadow-xl">
          {children}
        </div>
      </div>
    </div>
  );
}
