
from utils.db import instruments_collection

DEFAULT_INSTRUMENTS = [
    {"nombre": "Guitarra", "descripcion": "Cuerda"},
    {"nombre": "Piano", "descripcion": "Teclado"},
    {"nombre": "Bajo", "descripcion": "Cuerda grave"},
    {"nombre": "Batería", "descripcion": "Percusión"},
    {"nombre": "Violín", "descripcion": "Cuerda frotada"},
    {"nombre": "Viola", "descripcion": "Cuerda frotada"},
    {"nombre": "Cello", "descripcion": "Cuerda frotada grave"},
    {"nombre": "Flauta", "descripcion": "Viento-madera"},
    {"nombre": "Saxofón", "descripcion": "Viento-madera"},
    {"nombre": "Trompeta", "descripcion": "Viento-metal"},
    {"nombre": "Trombón", "descripcion": "Viento-metal"},
    {"nombre": "Clarinete", "descripcion": "Viento-madera"},
    {"nombre": "Ukelele", "descripcion": "Cuerda"},
    {"nombre": "Sintetizador", "descripcion": "Electrónico"},
    {"nombre": "Percusión latina", "descripcion": "Congas, bongó"}
]

def seed_instruments():
    if instruments_collection.estimated_document_count() == 0:
        instruments_collection.insert_many(DEFAULT_INSTRUMENTS)
        return {"seeded": len(DEFAULT_INSTRUMENTS)}
    return {"seeded": 0}
