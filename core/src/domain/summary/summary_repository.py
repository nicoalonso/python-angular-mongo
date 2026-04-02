from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from src.domain.summary import Summary


class SummaryRepository(ListRepository[Summary], ABC):
    """
    Summary Repository Interface
    """
    @abstractmethod
    async def obtain_by_url(self, url: str) -> Summary | None: ...
