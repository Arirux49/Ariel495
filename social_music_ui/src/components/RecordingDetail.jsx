import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import AppShell from "./layout/AppShell";
import Card from "./ui/Card";
import recordingsService from "../services/recordingsService";
import CommentThread from "./CommentThread";

export default function RecordingDetail() {
  const { id } = useParams();
  const [rec, setRec] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const data = await recordingsService.get(id);
        setRec(data);
      } catch (e) {
        setError(e.message || "Error");
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  return (
    <AppShell title="Detalle de Grabación">
      {loading ? <p className="text-zinc-400">Cargando…</p> : error ? <p className="text-red-400">{error}</p> : (
        <div className="space-y-4">
          <Card>
            <h2 className="text-xl font-semibold">{rec?.titulo || rec?.title || "Grabación"}</h2>
            <p className="text-sm text-zinc-400">{rec?.descripcion || rec?.description || ""}</p>
          </Card>
          <Card>
            <CommentThread targetType="recording" targetId={id} />
          </Card>
        </div>
      )}
    </AppShell>
  );
}
