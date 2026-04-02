from fastapi import Depends

from src.application.provider.creator import ProviderCreate
from src.application.provider.eraser import ProviderDelete
from src.application.provider.list import ProviderList
from src.application.provider.reader import ProviderRead
from src.application.provider.updater import ProviderUpdate
from src.infrastructure.dependencies.repository import get_provider_repository, get_user_repository, \
    get_purchase_repository


def get_provider_list(repo_provider = Depends(get_provider_repository)) -> ProviderList:
    return ProviderList(repo_provider)


def get_provider_creator(
        repo_provider = Depends(get_provider_repository),
        repo_user = Depends(get_user_repository),
) -> ProviderCreate:
    return ProviderCreate(repo_provider, repo_user)


def get_provider_reader(repo_provider = Depends(get_provider_repository)) -> ProviderRead:
    return ProviderRead(repo_provider)


def get_provider_updater(
        repo_provider = Depends(get_provider_repository),
        repo_user = Depends(get_user_repository)
) -> ProviderUpdate:
    return ProviderUpdate(repo_provider, repo_user)


def get_provider_eraser(
        repo_provider = Depends(get_provider_repository),
        repo_purchase = Depends(get_purchase_repository),
) -> ProviderDelete:
    return ProviderDelete(repo_provider, repo_purchase)


__all__ = [
    "get_provider_list",
    "get_provider_creator",
    "get_provider_reader",
    "get_provider_updater",
    "get_provider_eraser",
]
