import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { isValidEmail, validatePassword, getPasswordStrength } from "../utils/validators";

const SignupScreen = () => {
  const [formData, setFormData] = useState({
    name: "",
    lastname: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (error) setError("");
  };

  const handleSignup = async () => {
    if (isSubmitting) return;

    setError("");
    setSuccess("");
    setIsSubmitting(true);

    if (!formData.name.trim()) {
      setError("El nombre es requerido");
      setIsSubmitting(false);
      return;
    }
    if (!formData.lastname.trim()) {
      setError("El apellido es requerido");
      setIsSubmitting(false);
      return;
    }
    if (!formData.email.trim()) {
      setError("El email es requerido");
      setIsSubmitting(false);
      return;
    }
    if (!isValidEmail(formData.email)) {
      setError("Por favor ingresa un email válido");
      setIsSubmitting(false);
      return;
    }

    const pwdValidation = validatePassword(formData.password);
    if (!pwdValidation.isValid) {
      setError(pwdValidation.message);
      setIsSubmitting(false);
      return;
    }
    if (formData.password !== formData.confirmPassword) {
      setError("Las contraseñas no coinciden");
      setIsSubmitting(false);
      return;
    }

    try {
      const ok = await register(
        formData.name,
        formData.lastname,
        formData.email,
        formData.password
      );
      if (ok) {
        setSuccess("¡Cuenta creada exitosamente! Redirigiendo al login...");
        setFormData({
          name: "",
          lastname: "",
          email: "",
          password: "",
          confirmPassword: "",
        });
        navigate("/login", { replace: true });
      }
    } catch (err) {
      console.error("Error en registro:", err);
      setError(err.message || "Error al crear la cuenta. Intenta nuevamente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const strength = getPasswordStrength(formData.password);

  return (
    <div className="min-h-screen bg-[#121212] flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-[#181818] text-neutral-100 border border-[#282828] rounded-lg shadow-xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-full bg-[#1DB954] flex items-center justify-center mx-auto mb-4 shadow">
            <span className="text-2xl text-black">🎵</span>
          </div>
          <h1 className="text-2xl font-bold">Social Music</h1>
          <p className="text-sm text-neutral-400">Crear cuenta nueva</p>
        </div>

        {/* Mensajes */}
        {error && (
          <div
            className={`mb-4 p-3 rounded-md border ${
              error.includes("email ya está registrado") ||
              error.includes("usuario ya existe")
                ? "bg-amber-500/10 border-amber-400/40 text-amber-300"
                : "bg-red-500/10 border-red-400/40 text-red-300"
            }`}
          >
            <div className="flex items-center gap-2">
              <span>
                {error.includes("email ya está registrado") ||
                error.includes("usuario ya existe")
                  ? "⚠️"
                  : "❌"}
              </span>
              <span>{error}</span>
            </div>
            {(error.includes("email ya está registrado") ||
              error.includes("usuario ya existe")) && (
              <div className="mt-2 text-sm">
                <Link to="/login" className="text-[#1DB954] hover:text-[#1ed760] underline">
                  ¿Ya tienes cuenta? Inicia sesión aquí
                </Link>
              </div>
            )}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 rounded-md border border-emerald-400/40 bg-emerald-500/10 text-emerald-300">
            <div className="flex items-center gap-2">
              <span>✅</span>
              <span>{success}</span>
            </div>
          </div>
        )}

        {/* Formulario */}
        <form className="space-y-4" noValidate>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-neutral-200 mb-1">
                Nombre
              </label>
              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Juan"
                className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                           border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
              />
            </div>
            <div>
              <label htmlFor="lastname" className="block text-sm font-medium text-neutral-200 mb-1">
                Apellido
              </label>
              <input
                id="lastname"
                name="lastname"
                type="text"
                value={formData.lastname}
                onChange={handleChange}
                required
                placeholder="Pérez"
                className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                           border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-neutral-200 mb-1">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="usuario2@example.com"
              className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                         border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-neutral-200 mb-1">
              Contraseña
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="8-64 caracteres, 1 mayúscula, 1 número, 1 especial"
              className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                         border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
            />

            {formData.password && (
              <div className="mt-2 space-y-1">
                <div className="text-xs text-neutral-400 mb-1">Requisitos de contraseña:</div>
                <div className={`text-xs flex items-center ${strength.isValidLength ? "text-emerald-400" : "text-neutral-500"}`}>
                  <span className="mr-1">{strength.isValidLength ? "✓" : "○"}</span>8-64 caracteres
                </div>
                <div className={`text-xs flex items-center ${strength.hasUppercase ? "text-emerald-400" : "text-neutral-500"}`}>
                  <span className="mr-1">{strength.hasUppercase ? "✓" : "○"}</span>Al menos una mayúscula
                </div>
                <div className={`text-xs flex items-center ${strength.hasNumber ? "text-emerald-400" : "text-neutral-500"}`}>
                  <span className="mr-1">{strength.hasNumber ? "✓" : "○"}</span>Al menos un número
                </div>
                <div className={`text-xs flex items-center ${strength.hasSpecialChar ? "text-emerald-400" : "text-neutral-500"}`}>
                  <span className="mr-1">{strength.hasSpecialChar ? "✓" : "○"}</span>Carácter especial (@$!%*?&)
                </div>
              </div>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-neutral-200 mb-1">
              Confirmar Contraseña
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              placeholder="Confirma tu contraseña"
              onKeyDown={(e) => e.key === "Enter" && handleSignup()}
              className="w-full px-3 py-2 rounded-md bg-[#222] text-neutral-100 placeholder-neutral-500
                         border border-[#333] focus:outline-none focus:ring-2 focus:ring-[#1DB954] focus:border-transparent"
            />
          </div>

          <button
            type="button"
            onClick={handleSignup}
            disabled={isSubmitting}
            className="w-full bg-[#1DB954] text-black py-2 px-4 rounded-md hover:bg-[#1ed760] font-medium
                       disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {isSubmitting ? "Creando cuenta..." : "Crear Cuenta"}
          </button>
        </form>

        <p className="text-center text-sm text-neutral-400 mt-4">
          ¿Ya tienes cuenta?{" "}
          <Link to="/login" className="text-[#1DB954] hover:text-[#1ed760]">
            Inicia sesión
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignupScreen;
