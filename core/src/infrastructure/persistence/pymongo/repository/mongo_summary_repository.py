from dataclasses import asdict

from src.domain.summary import Summary, SummaryRepository
from src.infrastructure.persistence.pymongo.mapping import SummaryDocument
from .mongo_repository import MongoRepository


class MongoSummaryRepository(MongoRepository[Summary], SummaryRepository):
    """
    Repository for Summary entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["summaries"], model=SummaryDocument)

    async def obtain_by_url(self, url: str) -> Summary | None:
        return await self._find_one_by({"url": url})

    def _prime(self, element: Summary) -> dict:
        item = asdict(element)
        item["type"] = element.type.value
        item["state"] = element.state.value
        # noinspection PyArgumentList
        return self.model(**item).to_db()
