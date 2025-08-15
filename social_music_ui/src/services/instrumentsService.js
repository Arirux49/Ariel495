import { API_BASE_URL, handleResponse } from "./api";

const authHeader = () => {
  const t = localStorage.getItem("authToken");
  return t ? { Authorization: `Bearer ${t}` } : {};
};

const unwrapObjectId = (s) => {
  if (typeof s !== "string") return s;
  const m = s.match(/^ObjectId\(["']?([a-fA-F0-9]{24})["']?\)$/);
  return m ? m[1] : s;
};
const normId = (d) => {
  const raw = d?.id ?? d?._id?.$oid ?? d?._id;
  return raw ? String(unwrapObjectId(raw)) : null;
};

const instrumentsService = {
  async list(q) {
    const url = q
      ? `${API_BASE_URL}/instrumentos/search?q=${encodeURIComponent(q)}`
      : `${API_BASE_URL}/instrumentos/`; // slash final
    const r = await fetch(url, { headers: { ...authHeader() } });
    const data = await handleResponse(r);
    return (data || []).map((d) => ({
      ...d,
      id: normId(d),
      name: d?.name ?? d?.nombre ?? "",
      estado: d?.estado ?? "activo",
    }));
  },

  async create({ name }) {
    const r = await fetch(`${API_BASE_URL}/instrumentos/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ nombre: name }),
    });
    return handleResponse(r);
  },

  async update(id, { name }) {
    const safeId = String(unwrapObjectId(id ?? ""));
    const r = await fetch(`${API_BASE_URL}/instrumentos/${safeId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ nombre: name }),
    });
    return handleResponse(r);
  },

  async remove(id) {
    const safeId = String(unwrapObjectId(id ?? ""));
    const r = await fetch(`${API_BASE_URL}/instrumentos/${safeId}`, {
      method: "DELETE",
      headers: { ...authHeader() },
    });
    if (r.status === 409) {
      const data = await r.json().catch(() => ({}));
      throw new Error(data?.detail || "No se puede eliminar porque está en uso.");
    }
    return handleResponse(r);
  },
};

export default instrumentsService;
