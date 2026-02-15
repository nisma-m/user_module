import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "wallet_db")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

wallet_collection = db["wallets"]
