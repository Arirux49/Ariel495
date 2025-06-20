from bson.objectid import ObjectId
from conexion import db

class Estudiante:
    def __init__(self, nombre, cuenta, carrera):
        self.nombre = nombre
        self.cuenta = cuenta
        self.carrera = carrera
        self.carnet_id = None 

    def save(self):
        estudiante_doc = {
            "nombre": self.nombre,
            "cuenta": self.cuenta,
            "carrera": self.carrera,
            "carnet_id": self.carnet_id
        }
        result = db.estudiantes.insert_one(estudiante_doc)
        self._id = result.inserted_id
        return self._id

    def actualizar_carnet(self, carnet_id):
        result = db.estudiantes.update_one(
            {"_id": ObjectId(self._id)},
            {"$set": {"carnet_id": ObjectId(carnet_id)}}
        )
        print(f"Documentos actualizados: {result.modified_count}")
