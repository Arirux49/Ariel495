// src/components/SamplesPage.jsx
import { useEffect, useMemo, useState } from "react";
import samplesService from "../services/samplesService";
import instrumentsService from "../services/instrumentsService";

export default function SamplesPage() {
  const [title, setTitle] = useState("");
  const [instrumentId, setInstrumentId] = useState("");
  const [rawList, setRawList] = useState([]);
  const [rawTypes, setRawTypes] = useState([]);
  const [msg, setMsg] = useState("");

  const load = async () => {
    const [l, t] = await Promise.all([
      samplesService.list(),
      instrumentsService.list(),
    ]);
    setRawList(l || []);
    setRawTypes(t || []);
  };
  useEffect(() => { load(); }, []);

  const tipos = useMemo(() => {
    return (rawTypes || []).map((it) => ({
      id: it.id || it._id || it._id?.$oid || it._id,
      name: it.name || it.nombre || "",
    }));
  }, [rawTypes]);

  const list = useMemo(() => {
    return (rawList || []).map((it) => ({
      id: it.id || it._id || it._id?.$oid || it._id,
      title: it.title || it.nombre || it.file_name || "Sample",
      instrument_ids: it.instrument_ids || it.instrumentos || [],
      instrument_id: it.instrument_id,
      instrument_name: it.instrument_name || it.instrumento || it.instrument || "",
    }));
  }, [rawList]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await samplesService.create({ title: title.trim(), instrumentId });
    setTitle("");
    setInstrumentId("");
    setMsg("Sample creado.");
    load();
  };

  const handleUpdate = async (it) => {
    const nuevo = prompt("Nuevo título:", it.title);
    if (!nuevo || !nuevo.trim()) return;
    await samplesService.update(it.id, { title: nuevo.trim() });
    setMsg("Sample actualizado.");
    load();
  };

  const handleDelete = async (it) => {
    if (!confirm(`¿Eliminar '${it.title}'?`)) return;
    await samplesService.remove(it.id);
    setMsg("Sample eliminado.");
    load();
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-extrabold mb-2">Samples</h1>
        <p className="text-gray-400">CRUD usando /samples (y asignación de instrumento).</p>
      </div>

      <form onSubmit={handleCreate} className="card p-6 space-y-4">
        <div className="grid md:grid-cols-3 gap-4">
          <input
            className="input"
            placeholder="Título"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <select
            className="input"
            value={instrumentId}
            onChange={(e) => setInstrumentId(e.target.value)}
          >
            <option value="">(Opcional) Instrumento…</option>
            {tipos.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name}
              </option>
            ))}
          </select>
          <button className="btn-green">Crear</button>
        </div>
      </form>

      {msg && <div className="text-green-400 text-sm">{msg}</div>}

      <div className="card p-6">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left">
            <thead>
              <tr className="text-gray-400">
                <th className="py-2 pr-4">Título</th>
                <th className="py-2 pr-4">Instrumento(s)</th>
                <th className="py-2 pr-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {list.map((it) => (
                <tr key={it.id} className="border-t border-gray-800">
                  <td className="py-2 pr-4">{it.title}</td>
                  <td className="py-2 pr-4">
                    {it.instrument_name
                      ? it.instrument_name
                      : (it.instrument_ids || []).join(", ") || it.instrument_id || "—"}
                  </td>
                  <td className="py-2 pr-4 flex gap-2">
                    <button className="btn-secondary" onClick={() => handleUpdate(it)}>
                      Editar
                    </button>
                    <button className="btn-danger" onClick={() => handleDelete(it)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
              {list.length === 0 && (
                <tr>
                  <td colSpan="3" className="py-4 text-gray-500">
                    Sin registros.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
