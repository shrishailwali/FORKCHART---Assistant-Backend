from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "chat_app"
CHAT_COLLECTION_NAME = "chat_contents"

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
chat_collection: Collection = db[CHAT_COLLECTION_NAME]
