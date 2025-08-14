from typing import Any, Optional
from bson import ObjectId

def parse_object_id(raw: Any) -> Optional[ObjectId]:
    """Parse a Mongo ObjectId from various shapes.
    Supports:
      - '64f...abc' (str)
      - {'$oid': '64f...abc'}
      - {'_id': '64f...abc'}  (returns ObjectId of value)
    Returns None if impossible.
    """
    if raw is None:
        return None
    try:
        # if it's already an ObjectId
        if isinstance(raw, ObjectId):
            return raw
        # string
        if isinstance(raw, str):
            return ObjectId(raw)
        # dict with $oid
        if isinstance(raw, dict):
            if '$oid' in raw:
                return ObjectId(raw['$oid'])
            # nested _id or id
            if '_id' in raw and isinstance(raw['_id'], (str, dict, ObjectId)):
                return parse_object_id(raw['_id'])
            if 'id' in raw and isinstance(raw['id'], (str, dict, ObjectId)):
                return parse_object_id(raw['id'])
        # fallback
        s = str(raw)
        return ObjectId(s)
    except Exception:
        return None
