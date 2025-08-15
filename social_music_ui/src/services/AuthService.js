import { API_BASE_URL, handleResponse } from "./api.js";

const decodeToken = (token) => {
  const base64Url = token.split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
      .join("")
  );
  return JSON.parse(jsonPayload);
};

export const authService = {
  login: async (email, password) => {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await handleResponse(res);
    if (data?.access_token) {
      localStorage.setItem("authToken", data.access_token);
      localStorage.setItem("userInfo", JSON.stringify(decodeToken(data.access_token)));
    }
    return data;
  },

  // NOTA: dejamos el API en /auth/registro (también existe alias /users)
  register: async (name, lastname, email, password) => {
    const payload = {
      nombre: name,
      email,
      password,
      ...(lastname ? { perfil_artista: lastname } : {}),
    };
    const res = await fetch(`${API_BASE_URL}/auth/registro`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  logout: () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userInfo");
  },

  isAuthenticated: () => {
    const t = localStorage.getItem("authToken");
    if (!t) return false;
    try {
      const u = decodeToken(t);
      return u.exp * 1000 > Date.now();
    } catch {
      return false;
    }
  },

  getCurrentUser: () => {
    try {
      const u = localStorage.getItem("userInfo");
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },

  getToken: () => localStorage.getItem("authToken"),
};

export default authService;
