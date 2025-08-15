// src/components/InstrumentsPage.jsx
import { useEffect, useState } from "react";
import instrumentsService from "../services/instrumentsService";

export default function InstrumentsPage() {
  const [name, setName] = useState("");
  const [search, setSearch] = useState("");
  const [items, setItems] = useState([]);
  const [msg, setMsg] = useState("");
  const [msgErr, setMsgErr] = useState("");

  const load = async () => {
    setMsg(""); setMsgErr("");
    const data = await instrumentsService.list();
    // instrumentsService ya normaliza { id, name, estado }
    setItems(data || []);
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    try {
      await instrumentsService.create({ name: name.trim() });
      setName("");
      setMsg("Instrumento creado.");
    } catch (err) {
      setMsgErr(err?.message || "No se pudo crear el instrumento.");
    }
    load();
  };

  const handleUpdate = async (it) => {
    const nuevo = prompt("Nuevo nombre para el instrumento:", it.name);
    if (!nuevo || !nuevo.trim()) return;
    const safeId = String(it.id ?? it._id?.$oid ?? it._id ?? "");
    try {
      await instrumentsService.update(safeId, { name: nuevo.trim() });
      setMsg("Instrumento actualizado.");
    } catch (err) {
      setMsgErr(err?.message || "No se pudo actualizar.");
    }
    load();
  };

  const handleDelete = async (it) => {
    if (!confirm(`¿Eliminar '${it.name}'?`)) return;
    const safeId = String(it.id ?? it._id?.$oid ?? it._id ?? "");
    try {
      await instrumentsService.remove(safeId);
      setMsg("Instrumento eliminado.");
    } catch (err) {
      setMsgErr(err?.message || "No se pudo eliminar.");
    }
    load();
  };

  const filtered = (items || []).filter((i) =>
    !search.trim() || (i.name || "").toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-extrabold mb-2">Instrumentos</h1>
        <p className="text-gray-400">CRUD usando /instrumentos.</p>
      </div>

      <form onSubmit={handleCreate} className="card p-6 space-y-4">
        <div className="flex gap-3 items-center">
          <input
            className="input flex-1"
            placeholder="Nombre"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <button className="btn-green">Crear</button>
        </div>
      </form>

      {msg && <div className="text-green-400 text-sm">{msg}</div>}
      {msgErr && <div className="text-red-400 text-sm">{msgErr}</div>}

      <div className="card p-6 space-y-4">
        <div className="flex gap-3">
          <input
            className="input flex-1"
            placeholder="Buscar..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button className="btn-secondary" onClick={load}>
            Refrescar
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="min-w-full text-left">
            <thead>
              <tr className="text-gray-400">
                <th className="py-2 pr-4">Nombre</th>
                <th className="py-2 pr-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((it, idx) => (
                <tr key={it.id || idx} className="border-t border-gray-800">
                  <td className="py-2 pr-4">{it.name}</td>
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
              {filtered.length === 0 && (
                <tr>
                  <td colSpan="3" className="py-4 text-gray-500">
                    Sin resultados.
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
