from pymongo import AsyncMongoClient


class MongoConnection:
    def __init__(self, uri: str, db_name: str):
        self._uri = uri
        self._db_name = db_name
        self._client: AsyncMongoClient | None = None
        self._db = None

    async def connect(self) -> None:
        self._client = AsyncMongoClient(self._uri)
        self._db = self._client[self._db_name]
        await self._client.admin.command("ping")

    async def disconnect(self) -> None:
        if self._client is not None:
            await self._client.close()

    @property
    def db(self):
        if self._db is None:
            raise RuntimeError("Mongo DB no inicializada")
        return self._db
