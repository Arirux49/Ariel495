# Importamos el modelo base y el validador personalizado para ObjectId
from .base import ModeloBase, PyObjectId

# EmailStr valida que el campo tenga formato de correo electrónico, Field permite validaciones adicionales
from pydantic import EmailStr, Field

# List para listas tipadas, Optional para campos opcionales
from typing import List, Optional


# Modelo usado para el login de usuarios (entrada de email y password)
class UserLogin(ModeloBase):
    email: EmailStr  # Debe ser un email válido
    password: str    # Contraseña del usuario


# Modelo usado para registrar un nuevo usuario
class UserRegister(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    # Nombre del usuario (obligatorio, al menos 2 caracteres)

    email: EmailStr
    # Correo electrónico válido

    password: str = Field(..., min_length=8)
    # Contraseña con mínimo 8 caracteres

    perfil_artista: Optional[str] = Field(default="")
    # Campo opcional para perfil del artista (bio, descripción, etc.)


# Modelo base que define los atributos comunes del usuario
class UsuarioBase(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    # Nombre del usuario

    email: EmailStr
    # Correo electrónico

    perfil_artista: Optional[str] = Field(default="")
    # Descripción corta o bio del usuario


# Modelo para crear un usuario (extiende UsuarioBase y añade la contraseña)
class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)
    # La contraseña es requerida al crear usuario


# Modelo para actualizar parcialmente los datos del usuario
class UsuarioUpdate(ModeloBase):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    # Nombre es opcional al actualizar, pero si se da, mínimo 2 caracteres

    perfil_artista: Optional[str] = Field(default="")
    # Perfil opcional al actualizar


# Modelo que representa un usuario en la base de datos
class UsuarioDB(UsuarioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # ID de MongoDB, alias para compatibilidad con _id

    instrumentos: List[PyObjectId] = Field(default_factory=list)
    # Lista de instrumentos que el usuario toca (relación muchos a muchos)

    firebase_uid: str
    # UID único generado por Firebase Authentication


# Modelo que se retorna como respuesta al cliente
class UsuarioResponse(UsuarioBase):
    id: str = Field(..., alias="_id")
    # ID convertido a string para uso en frontend/API
