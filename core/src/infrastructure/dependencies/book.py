from fastapi import Depends

from src.application.book.available import BookAvailable
from src.application.book.creator import BookCreate
from src.application.book.eraser import BookDelete
from src.application.book.list import BookList
from src.application.book.reader import BookRead
from src.application.book.updater import BookUpdate
from src.infrastructure.dependencies.domain import get_inspect_factory
from src.infrastructure.dependencies.repository import *


def get_book_lister(repo_book = Depends(get_book_repository)) -> BookList:
    return BookList(repo_book)


def get_book_creator(
        repo_book = Depends(get_book_repository),
        repo_author = Depends(get_author_repository),
        repo_editorial = Depends(get_editorial_repository),
        repo_user = Depends(get_user_repository),
) -> BookCreate:
    return BookCreate(repo_book, repo_author, repo_editorial, repo_user)


def get_book_reader(repo_book = Depends(get_book_repository)) -> BookRead:
    return BookRead(repo_book)


def get_book_updater(
        repo_book = Depends(get_book_repository),
        repo_author = Depends(get_author_repository),
        repo_editorial = Depends(get_editorial_repository),
        repo_user = Depends(get_user_repository)
) -> BookUpdate:
    return BookUpdate(repo_book, repo_author, repo_editorial, repo_user)


def get_book_eraser(
        repo_book = Depends(get_book_repository),
        repo_purchase_line = Depends(get_purchase_line_repository),
        repo_sale_line = Depends(get_sale_line_repository),
        repo_borrow_line = Depends(get_borrow_line_repository),
) -> BookDelete:
    return BookDelete(
        repo_book,
        repo_purchase_line,
        repo_sale_line,
        repo_borrow_line,
    )


def get_book_available(
    repo_book = Depends(get_book_repository),
    factory = Depends(get_inspect_factory),
):
    return BookAvailable(repo_book, factory)


__all__ = [
    "get_book_lister",
    "get_book_creator",
    "get_book_reader",
    "get_book_updater",
    "get_book_eraser",
    "get_book_available",
]
