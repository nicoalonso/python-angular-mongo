from fastapi import Depends

from src.application.author.creator import AuthorCreate
from src.application.author.eraser import AuthorDelete
from src.application.author.list import AuthorList
from src.application.author.reader import AuthorRead
from src.application.author.updater import AuthorUpdate
from src.infrastructure.dependencies.repository import get_author_repository, get_user_repository, get_book_repository


def get_author_list(repo_author = Depends(get_author_repository)) -> AuthorList:
    return AuthorList(repo_author)


def get_author_creator(
        repo_author = Depends(get_author_repository),
        repo_user = Depends(get_user_repository),
) -> AuthorCreate:
    return AuthorCreate(repo_author, repo_user)


def get_author_reader(repo_author = Depends(get_author_repository)) -> AuthorRead:
    return AuthorRead(repo_author)


def get_author_updater(
        repo_author = Depends(get_author_repository),
        repo_user = Depends(get_user_repository)
) -> AuthorUpdate:
    return AuthorUpdate(repo_author, repo_user)


def get_author_eraser(
        repo_author = Depends(get_author_repository),
        repo_book = Depends(get_book_repository),
) -> AuthorDelete:
    return AuthorDelete(repo_author, repo_book)


__all__ = [
    "get_author_list",
    "get_author_creator",
    "get_author_reader",
    "get_author_updater",
    "get_author_eraser",
]
