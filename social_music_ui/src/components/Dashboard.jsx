// src/components/Dashboard.jsx
import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-extrabold mb-2">Dashboard</h1>
        <p className="text-gray-400">Gestiona tu música con estilo verde/negro.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        <div className="card p-6">
          <h2 className="text-xl font-semibold">Usuarios</h2>
          <p className="text-gray-400 mt-1">Consulta y administración básica.</p>
          <Link to="/users" className="btn-green mt-4 inline-block">Ir a Usuarios</Link>
        </div>

        <div className="card p-6">
          <h2 className="text-xl font-semibold">Instrumentos</h2>
          <p className="text-gray-400 mt-1">CRUD con eliminación segura.</p>
          <Link to="/instruments" className="btn-green mt-4 inline-block">Ir a Instrumentos</Link>
        </div>

        <div className="card p-6">
          <h2 className="text-xl font-semibold">Grabaciones</h2>
          <p className="text-gray-400 mt-1">Sección de comentarios (placeholder).</p>
          <Link to="/recordings" className="btn-green mt-4 inline-block">Ir a Comentarios</Link>
        </div>

        <div className="card p-6 md:col-span-2 xl:col-span-3">
          <h2 className="text-xl font-semibold">Samples</h2>
          <p className="text-gray-400 mt-1">CRUD y relación con instrumentos.</p>
          <Link to="/samples" className="btn-green mt-4 inline-block">Ir a Samples</Link>
        </div>
      </div>
    </div>
  );
}
