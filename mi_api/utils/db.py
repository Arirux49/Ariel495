from pymongo import MongoClient

client = MongoClient("mongodb+srv://Arirux:ariel123@cluster0.vcs8lnn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["social_music"]

users_collection = db["users"]
instruments_collection = db["instruments"]
samples_collection = db["samples"]
recordings_collection = db["recordings"]
comments_collection = db["comments"]

user_instruments = db["user_instruments"]
sample_instruments = db["sample_instruments"]
recording_samples = db["recording_samples"]

def ping_db():
    try:
        client.admin.command('ping')
        return True
    except Exception as e:
        print(f"Error de conexión a MongoDB: {e}")
        return False