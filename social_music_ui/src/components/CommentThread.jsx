import { useEffect, useState } from "react";
import commentsService from "../services/commentsService";

export default function CommentThread({ targetType, targetId }) {
  const [items, setItems] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    try {
      setLoading(true);
      const data = await commentsService.list({ targetType, targetId });
      setItems(Array.isArray(data) ? data : data.items || []);
      setError("");
    } catch (e) {
      setError(e.message || "Error al cargar comentarios");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [targetType, targetId]);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    try {
      await commentsService.create({ text, targetType, targetId });
      setText("");
      await load();
    } catch (e) {
      setError(e.message || "Error al publicar comentario");
    }
  };

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold">Comentarios</h3>
      {loading ? (
        <p className="text-zinc-400 text-sm">Cargando…</p>
      ) : (
        <ul className="space-y-2">
          {items.length === 0 && <li className="text-zinc-400 text-sm">Sin comentarios todavía</li>}
          {items.map((c) => (
            <li key={c.id || c._id} className="border border-zinc-800 rounded-xl p-3 bg-zinc-900/40">
              <p className="text-sm">{c.texto || c.text}</p>
              <p className="text-[11px] text-zinc-400 mt-1">{c.user_email || c.author || "Anónimo"}</p>
            </li>
          ))}
        </ul>
      )}

      <form onSubmit={onSubmit} className="flex gap-2">
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Escribe un comentario…"
          className="flex-1 rounded-xl bg-zinc-900 border border-zinc-800 px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-emerald-500/50"
        />
        <button
          type="submit"
          className="rounded-xl bg-emerald-500 text-black px-4 py-2 text-sm font-semibold hover:bg-emerald-400"
        >
          Publicar
        </button>
      </form>

      {error && <p className="text-red-400 text-sm">{error}</p>}
    </div>
  );
}
