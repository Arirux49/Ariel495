import { API_BASE_URL, handleResponse } from "./api";

const authHeader = () => {
  const t = localStorage.getItem("authToken");
  return t ? { Authorization: `Bearer ${t}` } : {};
};

const commentsService = {
  async list({ targetType, targetId }) {
    const r = await fetch(
      `${API_BASE_URL}/comentarios?target_type=${encodeURIComponent(targetType)}&target_id=${encodeURIComponent(targetId)}`,
      { headers: { "Content-Type": "application/json", ...authHeader() } }
    );
    return handleResponse(r);
  },
  async create({ text, targetType, targetId }) {
    const r = await fetch(`${API_BASE_URL}/comentarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ texto: text, target_type: targetType, target_id: targetId }),
    });
    return handleResponse(r);
  },
};

export default commentsService;
