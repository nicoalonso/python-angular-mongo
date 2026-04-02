from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

from pydantic import BaseModel

from src.domain.identity import Identity

T = TypeVar('T', bound='Identity')


class MongoDocument(BaseModel, Generic[T], ABC):
    @abstractmethod
    def to_domain(self) -> T: ...

    def to_db(self) -> dict[str, Any]:
        """
        Converts the AuthorDocument to a dictionary suitable for MongoDB storage.
        :return: (dict) document for MongoDB.
        """
        return self.model_dump(by_alias=True)
