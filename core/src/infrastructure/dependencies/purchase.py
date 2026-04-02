from fastapi import Depends

from src.application.purchase.creator.purchase_create import PurchaseCreate
from src.application.purchase.eraser import PurchaseDelete
from src.application.purchase.list import PurchaseList
from src.application.purchase.reader import PurchaseRead
from src.application.purchase.supplier import PurchaseSupply, PurchaseSupplyHandler
from src.application.purchase.updater import PurchaseUpdate
from src.infrastructure.dependencies.bus import get_bus
from src.infrastructure.dependencies.repository import *


def get_purchase_list(repo_purchase = Depends(get_purchase_repository)) -> PurchaseList:
    return PurchaseList(repo_purchase)


def get_purchase_creator(
        repo_purchase = Depends(get_purchase_repository),
        repo_purchase_line = Depends(get_purchase_line_repository),
        repo_provider = Depends(get_provider_repository),
        repo_book = Depends(get_book_repository),
        repo_user = Depends(get_user_repository),
        bus = Depends(get_bus),
) -> PurchaseCreate:
    return PurchaseCreate(
        repo_purchase=repo_purchase,
        repo_purchase_line=repo_purchase_line,
        repo_provider=repo_provider,
        repo_book=repo_book,
        repo_user=repo_user,
        bus=bus,
    )


def get_purchase_reader(
        repo_purchase = Depends(get_purchase_repository),
        repo_purchase_line = Depends(get_purchase_line_repository),
) -> PurchaseRead:
    return PurchaseRead(repo_purchase, repo_purchase_line)


def get_purchase_updater(
        repo_purchase = Depends(get_purchase_repository),
        repo_purchase_line = Depends(get_purchase_line_repository),
        repo_provider = Depends(get_provider_repository),
        repo_book = Depends(get_book_repository),
        repo_user = Depends(get_user_repository),
        bus = Depends(get_bus),
) -> PurchaseUpdate:
    return PurchaseUpdate(
        repo_purchase=repo_purchase,
        repo_purchase_line=repo_purchase_line,
        repo_provider=repo_provider,
        repo_book=repo_book,
        repo_user=repo_user,
        bus=bus,
    )


def get_purchase_eraser(
        repo_purchase = Depends(get_purchase_repository),
        repo_purchase_line = Depends(get_purchase_line_repository),
        bus = Depends(get_bus),
) -> PurchaseDelete:
    return PurchaseDelete(
        repo_purchase,
        repo_purchase_line,
        bus=bus,
    )


def get_purchase_supply(
        bus = Depends(get_bus),
) -> PurchaseSupply:
    return PurchaseSupply(bus)


def get_purchase_supply_handler(
        consumer = Depends(get_purchase_supply),
) -> PurchaseSupplyHandler:
    return PurchaseSupplyHandler(consumer)


__all__ = [
    "get_purchase_list",
    "get_purchase_creator",
    "get_purchase_reader",
    "get_purchase_updater",
    "get_purchase_eraser",
    "get_purchase_supply_handler",
]
