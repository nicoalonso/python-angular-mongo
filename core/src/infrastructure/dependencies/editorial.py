from fastapi import Depends

from src.application.editorial.creator import EditorialCreate
from src.application.editorial.eraser import EditorialDelete
from src.application.editorial.list import EditorialList
from src.application.editorial.reader import EditorialRead
from src.application.editorial.updater import EditorialUpdate
from src.infrastructure.dependencies.repository import get_editorial_repository, get_book_repository, get_user_repository


def get_editorial_list(repo_editorial = Depends(get_editorial_repository)) -> EditorialList:
    return EditorialList(repo_editorial)


def get_editorial_creator(
        repo_editorial = Depends(get_editorial_repository),
        repo_user = Depends(get_user_repository),
) -> EditorialCreate:
    return EditorialCreate(repo_editorial, repo_user)


def get_editorial_reader(repo_editorial = Depends(get_editorial_repository)) -> EditorialRead:
    return EditorialRead(repo_editorial)


def get_editorial_updater(
        repo_editorial = Depends(get_editorial_repository),
        repo_user = Depends(get_user_repository)
) -> EditorialUpdate:
    return EditorialUpdate(repo_editorial, repo_user)


def get_editorial_eraser(
        repo_editorial = Depends(get_editorial_repository),
        repo_book = Depends(get_book_repository),
) -> EditorialDelete:
    return EditorialDelete(repo_editorial, repo_book)


__all__ = [
    "get_editorial_list",
    "get_editorial_creator",
    "get_editorial_reader",
    "get_editorial_updater",
    "get_editorial_eraser",
]
