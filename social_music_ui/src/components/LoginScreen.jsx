import { useState } from "react";
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext";


const LoginScreen = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (isSubmitting) return;

    setError("");
    setIsSubmitting(true);

    if (!email.trim()) { setError("El email es requerido"); setIsSubmitting(false); return; }
    if (!email.includes("@") || !email.includes(".")) { setError("Por favor ingresa un email válido"); setIsSubmitting(false); return; }
    if (!password.trim()) { setError("La contraseña es requerida"); setIsSubmitting(false); return; }

    try {
      const result = await login(email, password);
      if (result) navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Error al iniciar sesión. Intenta nuevamente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#121212] flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-[#181818] text-neutral-100 border border-[#282828] rounded-lg shadow-xl p-8">
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-[#1DB954] flex items-center justify-center mx-auto mb-4 shadow">
            <span className="text-2xl text-black">🎵</span>
          </div>
          <h1 className="text-2xl font-bold">Social Music</h1>
          <p className="text-sm text-neutral-400">Inicia sesión</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-md border border-red-500/40 bg-red-500/10 text-red-300">
            <div className="flex items-center gap-2">
              <span>❌</span><span>{error}</span>
            </div>
          </div>
        )}

        <form className="space-y-4" noValidate>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-neutral-200 mb-1">Email</label>
            <input
              id="email"
              type="email"
              required
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); if (error) setError(""); }}
              onKeyDown={(e) => e.key === "Enter" && handleLogin()}
              className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                         border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-neutral-200 mb-1">Contraseña</label>
            <input
              id="password"
              type="password"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => { setPassword(e.target.value); if (error) setError(""); }}
              onKeyDown={(e) => e.key === "Enter" && handleLogin()}
              className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                         border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
            />
          </div>

          <button
            type="button"
            onClick={handleLogin}
            disabled={isSubmitting}
            className="w-full py-2 rounded-md font-medium text-black bg-[#1DB954]
                       hover:bg-[#1ed760] transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? "Iniciando sesión..." : "Iniciar Sesión"}
          </button>
        </form>

        <p className="text-center text-sm text-neutral-400 mt-4">
          ¿No tienes cuenta?{" "}
          <Link to="/signup" className="text-[#1DB954] hover:text-[#1ed760]">Regístrate</Link>
        </p>
      </div>
    </div>
  );
};

export default LoginScreen;
