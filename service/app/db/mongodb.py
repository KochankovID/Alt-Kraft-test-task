from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoStorage:
    def __init__(self):
        self._db_name: str | None = None
        self._client: AsyncIOMotorClient | None = None

    async def set_up(self, db_url: str, db_name: str):
        self._db_name = db_name
        self._client = AsyncIOMotorClient(db_url)

    def get_mongo_db(self) -> AsyncIOMotorDatabase:
        if self._client:
            return self._client.get_database(self._db_name)
        else:
            raise RuntimeError(
                "MongoDB client was not initialized (try to call set_up)"
            )


mongo_storage = MongoStorage()


async def is_database_online(db=Depends(mongo_storage.get_mongo_db)):
    try:
        await db.command("serverStatus")
        return True
    except Exception:
        return False
