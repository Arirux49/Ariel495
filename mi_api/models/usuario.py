from .base import ModeloBase, PyObjectId
from pydantic import EmailStr, Field
from typing import List, Optional

class UserLogin(ModeloBase):
    email: EmailStr
    password: str

class UserRegister(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    perfil_artista: Optional[str] = Field(default="")

class UsuarioBase(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    perfil_artista: Optional[str] = Field(default="")

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)

class UsuarioUpdate(ModeloBase):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    perfil_artista: Optional[str] = Field(default="")

class UsuarioDB(UsuarioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    instrumentos: List[PyObjectId] = Field(default_factory=list)
    firebase_uid: str

class UsuarioResponse(UsuarioBase):
    id: str = Field(..., alias="_id")