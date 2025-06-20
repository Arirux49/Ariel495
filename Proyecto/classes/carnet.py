from bson.objectid import ObjectId
from conexion import db

class Carnet:
    def __init__(self, codigo, fecha_emision, fecha_expiracion, estudiante_id):
        self.codigo = codigo
        self.fecha_emision = fecha_emision
        self.fecha_expiracion = fecha_expiracion
        self.estudiante_id = estudiante_id 

    def save(self):
        carnet_doc = {
            "codigo": self.codigo,
            "fecha_emision": self.fecha_emision,
            "fecha_expiracion": self.fecha_expiracion,
            "estudiante_id": ObjectId(self.estudiante_id)
        }
        result = db.carnets.insert_one(carnet_doc)
        self._id = result.inserted_id
        return self._id
    