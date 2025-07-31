# Importación de clases y funciones necesarias
from pydantic import BaseModel, Field  # BaseModel es la clase base de Pydantic para validación de datos
from typing import Optional  # Para campos opcionales en modelos
from bson import ObjectId  # Tipo especial de MongoDB para IDs únicos
from datetime import datetime  # Para manejar fechas

# Clase personalizada que permite usar ObjectId como tipo válido en Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        # Este método es requerido por Pydantic para aplicar validadores personalizados
        yield cls.validate  # Registra el validador definido abajo

    @classmethod
    def validate(cls, v):
        # Valida que el valor proporcionado sea un ObjectId válido
        if not ObjectId.is_valid(v):  # Verifica si el valor tiene el formato correcto
            raise ValueError("Invalid ObjectId")  # Lanza un error si no es válido
        return ObjectId(v)  # Devuelve el ObjectId si es válido

    @classmethod
    def __modify_schema__(cls, field_schema):
        # Modifica el esquema para que se reconozca como tipo "string" en la documentación
        field_schema.update(type="string")

# Clase base para todos los modelos que usarán Pydantic y trabajarán con MongoDB
class ModeloBase(BaseModel):
    class Config:
        arbitrary_types_allowed = True  # Permite tipos personalizados como ObjectId
        json_encoders = {ObjectId: str}  # Convierte automáticamente ObjectId a string al serializar
        from_attributes = True  # Permite la creación de modelos a partir de atributos (útil para ORMs)
