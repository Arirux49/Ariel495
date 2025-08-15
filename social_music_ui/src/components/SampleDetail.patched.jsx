import { useParams } from "react-router-dom";
import AppShell from "./layout/AppShell";
import Card from "./ui/Card";
import CommentThread from "./CommentThread";

export default function SampleDetailPatched() {
  const { id } = useParams();
  return (
    <AppShell title="Detalle de Sample">
      <Card className="mb-4">
        {/* Mantén aquí tu información del sample (nombre, instrumentos asociados, etc.) */}
        <p className="text-sm text-zinc-400">Información del sample #{id}</p>
      </Card>
      <Card>
        <CommentThread targetType="sample" targetId={id} />
      </Card>
    </AppShell>
  );
}
