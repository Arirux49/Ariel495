
import { API_BASE_URL, handleResponse } from "./api";

const authHeader = () => {
  const t = localStorage.getItem("authToken");
  return t ? { Authorization: `Bearer ${t}` } : {};
};

const tipoService = {
  list: async (onlyActive = false) => {
    const url = `${API_BASE_URL}/tipo?onlyActive=${onlyActive ? 1 : 0}`;
    const r = await fetch(url, { headers: { ...authHeader() } });
    return handleResponse(r);
  },
  create: async (payload) => {
    const r = await fetch(`${API_BASE_URL}/tipo`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(payload),
    });
    return handleResponse(r);
  },
  update: async (id, payload) => {
    const r = await fetch(`${API_BASE_URL}/tipo/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(payload),
    });
    return handleResponse(r);
  },
  remove: async (id) => {
    const r = await fetch(`${API_BASE_URL}/tipo/${id}`, {
      method: "DELETE",
      headers: { ...authHeader() },
    });
    return handleResponse(r);
  },
};

export default tipoService;
