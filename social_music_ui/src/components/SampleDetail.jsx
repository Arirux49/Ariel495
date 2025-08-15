// src/components/SampleDetail.jsx
import { useEffect, useState } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { samplesService } from "../services/samplesService";

export default function SampleDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [sample, setSample] = useState(null);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");

  const load = async () => {
    try {
      const s = await samplesService.getOne(id);
      setSample(s);
    } catch {}
    try {
      const c = await samplesService.listComments(id);
      setComments(c);
    } catch {
      setComments([]);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  const send = async () => {
    if (!text.trim()) return;
    await samplesService.addComment(id, text).catch(() => {});
    setText("");
    await load();
  };

  const delComment = async (cid) => {
    await samplesService.deleteComment(id, cid).catch(() => {});
    await load();
  };

  const delSample = async () => {
    await samplesService.remove(id).catch(() => {});
    navigate("/samples", { replace: true });
  };

  if (!sample) return <div className="p-6">Cargando…</div>;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">{sample.nombre}</h2>
        <div className="flex gap-3">
          <Link to="/samples" className="text-emerald-700 hover:text-emerald-800">
            ← Volver a Samples
          </Link>
          <button
            type="button"
            onClick={delSample}
            className="text-red-600 hover:text-red-700"
          >
            Eliminar sample
          </button>
        </div>
      </div>

      <div className="text-gray-700">
        {sample.descripcion && <p>{sample.descripcion}</p>}
        <p className="text-sm text-gray-500 mt-1">
          Archivo: <span className="font-medium">{sample.archivo || "—"}</span> ·
          Duración: <span className="font-medium">{sample.duracion ?? "—"}s</span>
        </p>
      </div>

      <section>
        <h3 className="font-semibold mb-2">Comentarios</h3>

        {comments.length === 0 ? (
          <p className="text-sm text-gray-500">Sé el primero en comentar</p>
        ) : (
          <ul className="space-y-2">
            {comments.map((c) => (
              <li key={c._id || c.id} className="border rounded p-3">
                <div className="flex items-center justify-between">
                  <span>{c.contenido}</span>
                  <button
                    type="button"
                    onClick={() => delComment(c._id || c.id)}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    borrar
                  </button>
                </div>
                {c.creado_en && (
                  <div className="text-xs text-gray-400">
                    {new Date(c.creado_en).toLocaleString()}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}

        <div className="mt-3 flex gap-2">
          <input
            className="flex-1 border rounded px-3 py-2"
            placeholder="Escribe un comentario…"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            type="button"
            onClick={send}
            className="rounded bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700"
          >
            Enviar
          </button>
        </div>
      </section>
    </div>
  );
}
