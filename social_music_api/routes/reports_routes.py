
from fastapi import APIRouter
from utils.db import samples_collection

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/samples-with-instruments")
async def samples_with_instruments():
    pipeline = [
        {"$lookup": {"from": "sample_instruments","localField": "_id","foreignField": "sample_id","as": "relaciones"}},
        {"$unwind": {"path": "$relaciones", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {"from": "instruments","localField": "relaciones.instrumento_id","foreignField": "_id","as": "instrumento"}},
        {"$unwind": {"path": "$instrumento", "preserveNullAndEmptyArrays": True}},
        {"$group": {"_id": "$_id","nombre": {"$first": "$nombre"},"instrumentos": {"$addToSet": {"_id": "$instrumento._id", "nombre": "$instrumento.nombre"}}}},
        {"$project": {"_id": {"$toString": "$_id"},"nombre": 1,"instrumentos": {"$map": {"input": "$instrumentos","as": "i","in": {"_id": {"$toString": "$$i._id"}, "nombre": "$$i.nombre"}}}}}
    ]
    return list(samples_collection.aggregate(pipeline))

@router.get("/samples-stats")
async def samples_stats():
    pipeline = [
        {"$group": {"_id": "$usuario_creador","total_samples": {"$sum": 1},"avg_duracion": {"$avg": "$duracion"}}},
        {"$project": {"usuario_creador": {"$toString": "$_id"},"total_samples": 1,"avg_duracion": 1}},
        {"$sort": {"total_samples": -1}}
    ]
    return list(samples_collection.aggregate(pipeline))
