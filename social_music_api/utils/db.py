
from pymongo import MongoClient
from decouple import config

MONGODB_URI = config("MONGODB_URI")
DB_NAME = config("DATABASE_NAME", default="social_music")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

users_collection = db["users"]
instruments_collection = db["instruments"]
samples_collection = db["samples"]
recordings_collection = db["recordings"]
comments_collection = db["comments"]

user_instruments = db["user_instruments"]
sample_instruments = db["sample_instruments"]
recording_samples = db["recording_samples"]

def ping_db() -> bool:
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False
