# app/database/db.py
from pymongo import AsyncMongoClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "library_db")

client = AsyncMongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_collection = db["users"]
books_collection = db["books"]
borrowed_collection = db["borrowed_books"]
