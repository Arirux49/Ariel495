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

const service = {
  async list() {
    const r = await fetch(`${API_BASE_URL}/samples/`, {
      headers: { "Content-Type": "application/json", ...authHeader() },
    });
    const data = await handleResponse(r);
    return (data || []).map((d) => ({
      ...d,
      id: normId(d),
      title: d?.title ?? d?.nombre ?? d?.file_name ?? "Sample",
      instrument_ids: d?.instrument_ids ?? d?.instrumentos ?? [],
      instrument_id: d?.instrument_id ?? null,
      instrument_name: d?.instrument_name ?? d?.instrumento ?? d?.instrument ?? "",
    }));
  },

  async getOne(id) {
    const r = await fetch(`${API_BASE_URL}/samples/${id}`, {
      headers: { "Content-Type": "application/json", ...authHeader() },
    });
    return handleResponse(r);
  },

  async create({ title, instrumentId }) {
    const r = await fetch(`${API_BASE_URL}/samples/`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ title }),
    });
    const sample = await handleResponse(r);
    const sid = sample?.id ?? sample?._id?.$oid ?? sample?._id;

    if (sid && instrumentId) {
      const link = await fetch(`${API_BASE_URL}/samples/${sid}/instrumentos`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeader() },
        body: JSON.stringify({ instrumento_ids: [instrumentId] }),
      });
      await handleResponse(link);
    }
    return sample;
  },

  async update(id, { title }) {
    const r = await fetch(`${API_BASE_URL}/samples/${id}`, {
      method: "PATCH", // PATCH, no PUT
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ title }),
    });
    return handleResponse(r);
  },

  async remove(id) {
    const r = await fetch(`${API_BASE_URL}/samples/${id}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json", ...authHeader() },
    });
    return handleResponse(r);
  },

  async addInstruments(sampleId, instruments) {
    const r = await fetch(`${API_BASE_URL}/samples/${sampleId}/instrumentos`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ instrumento_ids: instruments }),
    });
    return handleResponse(r);
  },

  async listComments(sampleId) {
    const r = await fetch(`${API_BASE_URL}/samples/${sampleId}/comentarios`, {
      headers: { "Content-Type": "application/json", ...authHeader() },
    });
    return handleResponse(r);
  },

  async addComment(sampleId, texto) {
    const r = await fetch(`${API_BASE_URL}/samples/${sampleId}/comentarios`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ texto }),
    });
    return handleResponse(r);
  },
};

// exporto ambos para evitar pantalla en blanco por import
export const samplesService = service;
export default service;
