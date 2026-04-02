from fastapi import Depends

from src.application.borrow.checkin import BorrowCheckin
from src.application.borrow.creator import BorrowCreate
from src.application.borrow.list import BorrowList
from src.application.borrow.reader import BorrowRead
from src.infrastructure.dependencies.repository import *


def get_borrow_list(repo_borrow = Depends(get_borrow_repository)) -> BorrowList:
    return BorrowList(repo_borrow)

def get_borrow_creator(
        repo_borrow = Depends(get_borrow_repository),
        repo_borrow_line = Depends(get_borrow_line_repository),
        repo_customer = Depends(get_customer_repository),
        repo_book = Depends(get_book_repository),
        repo_sequence_number = Depends(get_sequence_number_repository),
        repo_user = Depends(get_user_repository),
) -> BorrowCreate:
    return BorrowCreate(
        repo_borrow=repo_borrow,
        repo_borrow_line=repo_borrow_line,
        repo_customer=repo_customer,
        repo_book=repo_book,
        repo_sequence_number=repo_sequence_number,
        repo_user=repo_user,
    )

def get_borrow_reader(
        repo_borrow = Depends(get_borrow_repository),
        repo_borrow_line = Depends(get_borrow_line_repository),
) -> BorrowRead:
    return BorrowRead(repo_borrow, repo_borrow_line)


def get_borrow_checker(
        repo_borrow = Depends(get_borrow_repository),
        repo_borrow_line = Depends(get_borrow_line_repository),
        repo_user = Depends(get_user_repository),
) -> BorrowCheckin:
    return BorrowCheckin(
        repo_borrow,
        repo_borrow_line,
        repo_user,
    )


__all__ = [
    "get_borrow_list",
    "get_borrow_creator",
    "get_borrow_reader",
    "get_borrow_checker",
]
