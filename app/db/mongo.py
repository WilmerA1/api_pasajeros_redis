from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from os import getenv
load_dotenv() 

MONGO_URI = getenv("MONGO_URI")
MONGO_DB_NAME = getenv("MONGO_DB_NAME")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]