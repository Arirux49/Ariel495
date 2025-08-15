const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").trim();

if (!API_BASE_URL) {
  // Ayuda en dev para detectar mala config
  // eslint-disable-next-line no-console
  console.warn(
    "[api] VITE_API_BASE_URL no está definida. Configúrala en tu .env (ej: http://127.0.0.1:8000)"
  );
}

const apiConfig = {
  headers: { "Content-Type": "application/json" },
};

// Manejo de errores consistente y útil en la UI
const handleResponse = async (response) => {
  if (!response.ok) {
    let detail = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      detail = data?.detail || data?.message || detail;
    } catch {
      // body vacío o no-JSON
    }

    // 401: solo “resetea” si había token (sesión expirada).
    // Si NO hay token (p.ej., login fallido), no redirigimos a /login automáticamente,
    // devolvemos el mensaje para mostrarlo en el formulario.
    if (response.status === 401) {
      const hadToken = !!localStorage.getItem("authToken");
      if (hadToken) {
        localStorage.removeItem("authToken");
        localStorage.removeItem("userInfo");
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        throw new Error(detail || "Tu sesión ha expirado. Inicia sesión nuevamente.");
      }
      // sin token: credenciales inválidas
      throw new Error(detail || "Correo o contraseña incorrectos");
    }

    if (response.status === 400) {
      throw new Error(detail || "Solicitud inválida");
    }
    if (response.status === 403) {
      throw new Error(detail || "No tienes permisos para realizar esta acción.");
    }
    if (response.status === 404) {
      throw new Error(detail || "Recurso no encontrado.");
    }
    if (response.status === 409) {
      throw new Error(detail || "Conflicto: el recurso ya existe.");
    }
    if (response.status >= 500) {
      throw new Error(detail || "Error interno del servidor.");
    }

    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
};

export { API_BASE_URL, apiConfig, handleResponse };
