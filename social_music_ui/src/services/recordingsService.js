import { API_BASE_URL, handleResponse } from "./api";

const authHeader = () => {
  const t = localStorage.getItem("authToken");
  return t ? { Authorization: `Bearer ${t}` } : {};
};

const recordingsService = {
  async list() {
    const r = await fetch(`${API_BASE_URL}/grabaciones`, { headers: { ...authHeader() } });
    return handleResponse(r);
  },
  async get(id) {
    const r = await fetch(`${API_BASE_URL}/grabaciones/${id}`, { headers: { ...authHeader() } });
    return handleResponse(r);
  },
  async create(payload) {
    const r = await fetch(`${API_BASE_URL}/grabaciones`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify(payload),
    });
    return handleResponse(r);
  },
  async addSamples(id, sampleIds) {
    const r = await fetch(`${API_BASE_URL}/grabaciones/${id}/samples`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ sample_ids: sampleIds }),
    });
    return handleResponse(r);
  },
  async remove(id) {
    const r = await fetch(`${API_BASE_URL}/grabaciones/${id}`, {
      method: "DELETE",
      headers: { ...authHeader() },
    });
    return handleResponse(r);
  },
};

export default recordingsService;
