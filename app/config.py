import os
from dotenv import load_dotenv

load_dotenv()

TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN")

EQUIPMENT_TYPES = [
    "dumbbell",
    "barbell",
    "bodyweight",
    "kettlebell",
    "medicine ball",
    "machine",
]
