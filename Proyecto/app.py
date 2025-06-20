from classes.estudiante import Estudiante
from classes.carnet import Carnet


est = Estudiante("Ariel González", "20221003375", "Ingeniería en Sistemas")
est_id = est.save()
print("Estudiante guardado con ID:", est_id)


carnet = Carnet("UNAH-2025-001", "2025-06-19", "2026-06-19", est_id)
carnet_id = carnet.save()
print("Carnet guardado con ID:", carnet_id)


est.actualizar_carnet(carnet_id)
print("Estudiante actualizado con carnet_id.")
