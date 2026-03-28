import random
import string
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# 🔧 Env config
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "krishi_dristi")
COLLECTION_NAME = os.getenv("USERS_COLLECTION", "users")

# ✅ Mongo connection (YOU MISSED THIS)
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db[COLLECTION_NAME]


# ─────────────────────────────────────────────
def username_exists(username: str) -> bool:
    return users.find_one({"username": username}) is not None


# ─────────────────────────────────────────────
def generate_suggestions(base_name: str, count: int = 5):
    suggestions = set()
    attempts = 0

    while len(suggestions) < count and attempts < 50:
        attempts += 1
        choice = random.randint(1, 4)

        if choice == 1:
            new_name = f"{base_name}{random.randint(10,9999)}"

        elif choice == 2:
            new_name = f"{base_name}_{random.randint(1,99)}"

        elif choice == 3:
            prefix = random.choice(["real", "the", "official", "its"])
            new_name = f"{prefix}_{base_name}"

        else:
            suffix = ''.join(random.choices(string.ascii_lowercase, k=3))
            new_name = f"{base_name}{suffix}"

        if not username_exists(new_name):
            suggestions.add(new_name)

    return list(suggestions)


# ─────────────────────────────────────────────
def check_and_suggest(username: str):
    username = username.lower().strip()

    if not username_exists(username):
        return {
            "available": True,
            "username": username,
            "suggestions": []
        }

    return {
        "available": False,
        "username": username,
        "suggestions": generate_suggestions(username)
    }