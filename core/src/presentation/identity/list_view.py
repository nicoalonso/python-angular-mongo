from dataclasses import asdict

from pydantic import BaseModel
from typing_extensions import TypeVar, Generic

from src.domain.identity.list import ListResult
from .pagination_view import PaginationView

T = TypeVar('T')


class ListView(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationView

    @staticmethod
    def serialize(result: ListResult, model: type[T]):
        """Serialize a ListResult to a ListView with the given model for items"""
        return ListView(
            items=result.items.map(lambda item: model(**asdict(item))).to_array(),
            pagination=PaginationView.serialize(result.pagination)
        )
