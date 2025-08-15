from typing import Any, Optional
from bson import ObjectId

def parse_object_id(raw: Any) -> Optional[ObjectId]:
    if raw is None: return None
    try:
        if isinstance(raw, ObjectId): return raw
        if isinstance(raw, str): return ObjectId(raw)
        if isinstance(raw, dict):
            if "$oid" in raw: return ObjectId(raw["$oid"])
            if "_id" in raw: return parse_object_id(raw["_id"])
            if "id" in raw: return parse_object_id(raw["id"])
        return ObjectId(str(raw))
    except Exception:
        return None
