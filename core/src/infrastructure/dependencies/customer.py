from fastapi import Depends

from src.application.customer.creator import CustomerCreate
from src.application.customer.eraser import CustomerDelete
from src.application.customer.list import CustomerList
from src.application.customer.reader.customer_read import CustomerRead
from src.application.customer.updater import CustomerUpdate
from src.infrastructure.dependencies.repository import *


def get_customer_list(repo_customer = Depends(get_customer_repository)) -> CustomerList:
    return CustomerList(repo_customer)


def get_customer_creator(
        repo_customer = Depends(get_customer_repository),
        repo_sequence_number = Depends(get_sequence_number_repository),
        repo_user = Depends(get_user_repository),
) -> CustomerCreate:
    return CustomerCreate(repo_customer, repo_sequence_number, repo_user)


def get_customer_reader(repo_customer = Depends(get_customer_repository)) -> CustomerRead:
    return CustomerRead(repo_customer)


def get_customer_updater(
        repo_customer = Depends(get_customer_repository),
        repo_user = Depends(get_user_repository)
) -> CustomerUpdate:
    return CustomerUpdate(repo_customer, repo_user)


def get_customer_eraser(
        repo_customer = Depends(get_customer_repository),
        repo_sale = Depends(get_sale_repository),
        repo_borrow = Depends(get_borrow_repository),
) -> CustomerDelete:
    return CustomerDelete(repo_customer, repo_sale, repo_borrow)


__all__ = [
    'get_customer_list',
    'get_customer_creator',
    'get_customer_reader',
    'get_customer_updater',
    'get_customer_eraser',
]
