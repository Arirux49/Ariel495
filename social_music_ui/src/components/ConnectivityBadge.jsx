import { useEffect, useState } from "react";
import { API, API_BASE_URL, API_PATH } from "../services/api";

export default function ConnectivityBadge() {
  const [status, setStatus] = useState("checking...");
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const r = await fetch(`${API}/health`);
        if (r.ok) {
          setStatus("ok");
          setErr("");
        } else {
          setStatus(`HTTP ${r.status}`);
          setErr(await r.text().catch(() => ""));
        }
      } catch (e) {
        setStatus("failed");
        setErr(e.message || "Failed to fetch");
      }
    })();
  }, []);

  return (
    <p className="text-[11px] text-zinc-500 mt-2">
      API: {API_BASE_URL || "N/A"}{API_PATH} · health: {status}
      {err ? ` · ${err}` : ""}
      · Token: {localStorage.getItem("authToken") ? "sí" : "no"}
    </p>
  );
}
