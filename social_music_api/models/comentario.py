
from pydantic import BaseModel, Field
from typing import Literal

class ComentarioCreate(BaseModel):
    texto: str = Field(..., min_length=1, max_length=500)
    target_type: Literal["sample","recording"]
    target_id: str
