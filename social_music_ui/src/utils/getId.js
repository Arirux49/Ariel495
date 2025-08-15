export function getMongoId(obj) {
  if (!obj) return "";
  if (typeof obj === "string") return obj;
  if (obj._id && typeof obj._id === "string") return obj._id;
  if (obj.id && typeof obj.id === "string") return obj.id;
  if (obj._id && typeof obj._id === "object" && obj._id.$oid) return obj._id.$oid;
  if (obj.id && typeof obj.id === "object" && obj.id.$oid) return obj.id.$oid;
  // fallback: try common variants
  const maybe = obj._id || obj.id;
  try {
    return String(maybe);
  } catch { return ""; }
}
