
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=60)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=60)
    perfil_artista: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    perfil_artista: Optional[str] = None

class UsuarioResponse(BaseModel):
    _id: str = Field(..., alias="_id")
    nombre: str
    email: EmailStr
    perfil_artista: Optional[str] = None
    class Config:
        allow_population_by_field_name = True
