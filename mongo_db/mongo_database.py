from datetime import datetime
from decouple import config
import certifi
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo_DB:
    log_collection = {
        "_id": "",
        "url": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }

    def __init__(self):
        self.client = AsyncIOMotorClient(
            config("MONGO_DB_URL"), tlsCAFile=certifi.where()
        )
        self.db = self.client.series_mongo_db
        self.collection = self.db.log_collection

    async def add_to_log_collection(self, log_objects):
        await self.collection.insert_one(log_objects)
