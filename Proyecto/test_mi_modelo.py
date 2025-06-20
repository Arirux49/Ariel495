import unittest
from classes.estudiante import Estudiante
from classes.carnet import Carnet
from conexion import db
from bson.objectid import ObjectId

class TestRelacionUnoAUno(unittest.TestCase):

    def setUp(self):
        # Limpiar colecciones antes de cada prueba
        db.estudiantes.delete_many({})
        db.carnets.delete_many({})

    def test_creacion_estudiante_y_carnet(self):
        # Crear y guardar estudiante
        est = Estudiante("Ariel Test", "202099999", "Ingeniería")
        est_id = est.save()

        # Crear y guardar carnet
        carnet = Carnet("TEST-0001", "2025-06-20", "2026-06-20", est_id)
        carnet_id = carnet.save()

        # Verificar que el carnet tiene el ID del estudiante
        carnet_en_db = db.carnets.find_one({"_id": ObjectId(carnet_id)})
        self.assertEqual(carnet_en_db["estudiante_id"], est_id)

    def test_actualizacion_estudiante_con_carnet(self):
        # Crear estudiante y carnet
        est = Estudiante("Ana Test", "202088888", "Derecho")
        est_id = est.save()

        carnet = Carnet("TEST-0002", "2025-01-01", "2026-01-01", est_id)
        carnet_id = carnet.save()

        # Actualizar estudiante
        est._id = est_id
        est.actualizar_carnet(carnet_id)

        # Verificar que el estudiante tiene el ID del carnet
        estudiante_en_db = db.estudiantes.find_one({"_id": ObjectId(est_id)})
        self.assertEqual(estudiante_en_db["carnet_id"], carnet_id)

if __name__ == '__main__':
    unittest.main()
