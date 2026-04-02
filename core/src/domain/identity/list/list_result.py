from typing import Generic, TypeVar, Optional

from src.domain.identity import Collection
from src.domain.identity.list import Pagination

T = TypeVar('T')


class ListResult(Generic[T]):
    """
    List result class

    :ivar items: Collection[T] - The list of items
    :ivar pagination: Pagination - The pagination information
    """
    def __init__(
            self,
            items: Optional[Collection[T]] = None,
            pagination: Optional[Pagination] = None,
    ):
        self.items: Collection[T] = items or Collection()
        self.pagination: Pagination = pagination or Pagination()
