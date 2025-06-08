from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from api.utilities.models import VoteResponse
from api.utils import Log

class DatabaseWrapper:
    """wrapper class for database connections"""

    def __init__(self, *, connection_string=None, url=None, port=None, database: str):
        """Provite either the databse uri/connection string or url and port along with the database name as kwargs"""

        if connection_string:
            self.client = AsyncIOMotorClient(connection_string)
        elif url and port:
            self.client = AsyncIOMotorClient(url, port)
        else:
            Log.warning("INVALID CONNECTION PARAMETERS PROVIDED")
            # raise Exception()


        self.database = self.client.get_database(database)

    async def add_to_collection(self, *, collection: str, data: dict):
        """inserts provided dictionary as it is into provided collection"""
        try:
            _collection: AsyncIOMotorCollection = self.database.get_collection(collection)
            insertion_response = await _collection.insert_one(data)
            if insertion_response.acknowledged:
                # insertion success
                return True
            else:
                return False
        except Exception as e:
            print(e)
            Log.warning(str(e))

    async def fetchResults(self, *, collection: str, query={}) -> list[VoteResponse]:
        """fetches all results as per query, query defaults to {} if nothing provided"""

        _collection: AsyncIOMotorCollection = self.database[collection]
        cursor = _collection.find(query)
        return await cursor.to_list()
