import redis.asyncio as redis
from datetime import datetime
from decouple import config
import json


class Redis_DB:
    redis_url_data = {
        "url": "",
        "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    }

    def __init__(self):
        self.connection_url = config("REDIS_URL")

    async def add_to_redis_db(self, redis_objects: dict):
        connection_url = await redis.from_url(self.connection_url)
        await connection_url.set("redis_dict", json.dumps(redis_objects), nx=True)
        # print(await connection_url.get("redis_dict"))

    # async def add_to_redis_db(self, redis_objects: dict):
    #     redis_url_data = {
    #         "url": "",
    #         "date": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
    #     }
    #     r = await redis.from_url(self.connection_url)
    #     await r.set("redis_dict", json.dumps(redis_objects))
