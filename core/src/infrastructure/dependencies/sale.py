from fastapi import Depends

from src.application.sale.consumer import SaleConsume, SaleConsumeHandler
from src.application.sale.creator import SaleCreate
from src.application.sale.list import SaleList
from src.application.sale.reader import SaleRead
from src.infrastructure.dependencies.bus import get_bus
from src.infrastructure.dependencies.repository import *


def get_sale_list(repo_sale = Depends(get_sale_repository)) -> SaleList:
    return SaleList(repo_sale)


def get_sale_creator(
        repo_sale = Depends(get_sale_repository),
        repo_sale_line = Depends(get_sale_line_repository),
        repo_customer = Depends(get_customer_repository),
        repo_book = Depends(get_book_repository),
        repo_sequence_number = Depends(get_sequence_number_repository),
        repo_user = Depends(get_user_repository),
        bus = Depends(get_bus),
) -> SaleCreate:
    return SaleCreate(
        repo_sale=repo_sale,
        repo_sale_line=repo_sale_line,
        repo_customer=repo_customer,
        repo_book=repo_book,
        repo_sequence_number=repo_sequence_number,
        repo_user=repo_user,
        bus=bus,
    )


def get_sale_reader(
        repo_sale = Depends(get_sale_repository),
        repo_sale_line = Depends(get_sale_line_repository),
) -> SaleRead:
    return SaleRead(repo_sale, repo_sale_line)


def get_sale_consume(
        bus = Depends(get_bus),
) -> SaleConsume:
    return SaleConsume(bus)


def get_sale_consume_handler(
        consumer = Depends(get_sale_consume),
) -> SaleConsumeHandler:
    return SaleConsumeHandler(consumer)


__all__ = [
    "get_sale_list",
    "get_sale_creator",
    "get_sale_reader",
    "get_sale_consume_handler",
]
