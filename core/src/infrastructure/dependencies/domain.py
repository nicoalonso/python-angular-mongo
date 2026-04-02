from fastapi import Depends

from src.domain.services.book_inspector import BookInspectFactory
from src.infrastructure.dependencies.repository import get_borrow_line_repository


def get_inspect_factory(repo_borrow_line = Depends(get_borrow_line_repository)) -> BookInspectFactory:
    return BookInspectFactory(repo_borrow_line)


__all__ = [
    "get_inspect_factory",
]
