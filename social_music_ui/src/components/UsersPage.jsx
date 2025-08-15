// src/components/UsersPage.jsx
import { useState } from "react";

export default function UsersPage() {
  const [userId, setUserId] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: conectar con tu endpoint de usuarios si aplica
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-extrabold mb-2">Usuarios</h1>
        <p className="text-gray-400">Gestiona tu música con estilo verde/negro.</p>
      </div>

      <form onSubmit={handleSubmit} className="card p-6 space-y-4">
        <div className="flex gap-4 items-center">
          <input
            className="input flex-1"
            placeholder="usuario_id"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <button type="submit" className="btn-green">Obtener usuario</button>
        </div>
      </form>
    </div>
  );
}
