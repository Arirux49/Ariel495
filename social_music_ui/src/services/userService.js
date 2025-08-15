// src/services/usersService.js
import { API_BASE_URL, handleResponse } from "./api";

// Header con token (si existe)
const authHeader = () => {
  const token = localStorage.getItem("authToken");
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const usersService = {
  // GET /usuarios/{usuario_id}
  async getById(usuarioId) {
    const res = await fetch(`${API_BASE_URL}/usuarios/${usuarioId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        ...authHeader(),
      },
    });
    return handleResponse(res);
  },

  // PUT /usuarios/{usuario_id}
  async update(usuarioId, data) {
    const res = await fetch(`${API_BASE_URL}/usuarios/${usuarioId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...authHeader(),
      },
      body: JSON.stringify(data),
    });
    return handleResponse(res);
  },

  // POST /usuarios/{usuario_id}/instrumentos
  // instruments: array de IDs de instrumentos (ajústalo a tu payload real)
  async addInstruments(usuarioId, instruments) {
    const res = await fetch(
      `${API_BASE_URL}/usuarios/${usuarioId}/instrumentos`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeader(),
        },
        body: JSON.stringify({ instruments }),
      }
    );
    return handleResponse(res);
  },
};

export default usersService;
