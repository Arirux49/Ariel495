# Importaciones necesarias
from fastapi import HTTPException, UploadFile  # Manejo de excepciones HTTP y archivos subidos
from typing import Dict, Any, List  # Tipos para tipado estático
from utils.db import samples_collection, sample_instruments, instruments_collection  # Colecciones de MongoDB
from utils.storage import upload_audio  # Función personalizada para subir archivos de audio
from bson import ObjectId  # Para manejar identificadores de MongoDB

# Definición del controlador de Sample
class SampleController:
    @staticmethod
    async def upload_sample(file: UploadFile, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Carga un archivo de audio como Sample, lo guarda en MongoDB y crea relaciones con instrumentos.

        Args:
            file: archivo de audio subido
            metadata: información adicional como nombre, usuario_id, duración, instrumentos

        Returns:
            Diccionario con los datos del Sample guardado
        """
        # Subimos el archivo de audio y obtenemos su URL
        url_archivo = await upload_audio(file)

        # Creamos el documento del sample
        sample = {
            "nombre": metadata["nombre"],  # Nombre del sample
            "usuario_creador": ObjectId(metadata["usuario_id"]),  # Convertimos el ID del usuario a ObjectId
            "archivo": url_archivo,  # URL del archivo
            "duracion": metadata.get("duracion")  # Puede ser opcional
        }

        # Insertamos el sample en la colección
        result = samples_collection.insert_one(sample)
        sample_id = result.inserted_id  # Obtenemos el ID generado

        # Asociamos el sample a los instrumentos especificados
        for instr_id in metadata.get("instrumentos_ids", []):
            if not instruments_collection.find_one({"_id": ObjectId(instr_id)}):
                raise HTTPException(404, f"Instrumento {instr_id} no existe")

            sample_instruments.insert_one({
                "sample_id": sample_id,
                "instrumento_id": ObjectId(instr_id)
            })

        # Convertimos el ID del sample a string para devolverlo al cliente
        sample["_id"] = str(sample_id)
        return sample

    @staticmethod
    def get_by_instrumento(instrumento_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene los samples asociados a un instrumento usando agregación en MongoDB.

        Args:
            instrumento_id: ID del instrumento

        Returns:
            Lista de samples vinculados con el instrumento
        """
        return list(samples_collection.aggregate([
            {
                "$lookup": {
                    "from": "sample_instruments",  # Relacionamos con esta colección
                    "localField": "_id",  # Campo local
                    "foreignField": "sample_id",  # Campo foráneo
                    "as": "relaciones"  # Nombre del array resultante
                }
            },
            { "$unwind": "$relaciones" },  # Aplanamos los arrays de relaciones
            {
                "$match": {
                    "relaciones.instrumento_id": ObjectId(instrumento_id)  # Filtramos por ID
                }
            },
            {
                "$project": {
                    "_id": { "$toString": "$_id" },  # Convertimos el ID a string
                    "nombre": 1,  # Incluimos nombre
                    "archivo": 1,  # Incluimos URL del archivo
                    "duracion": 1  # Incluimos duración
                }
            }
        ]))
