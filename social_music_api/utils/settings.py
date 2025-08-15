import os
from dotenv import load_dotenv

# Load .env if present (keeps your existing .env values)
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "social_music")
