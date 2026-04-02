from src.domain.provider import ProviderRepository
from src.domain.provider.exception import ProviderNotFoundError
from src.domain.purchase import PurchaseRepository
from .provider_associated_error import ProviderAssociatedError


class ProviderDelete:
    """
    Use case for deleting a provider from the system.
    """
    def __init__(
            self,
            repo_provider: ProviderRepository,
            repo_purchase: PurchaseRepository,
    ):
        self.repo_provider = repo_provider
        self.repo_purchase = repo_purchase

    async def dispatch(self, provider_id: str) -> None:
        """
        Deletes a provider by its ID.

        :param provider_id: The ID of the provider to be deleted.
        :raises ProviderNotFoundError: If the provider with the given ID does not exist.
        """
        provider = await self.repo_provider.obtain_by_id(provider_id)
        if not provider:
            raise ProviderNotFoundError(provider_id)

        purchases = await self.repo_purchase.obtain_by_provider(provider_id, 1)
        if not purchases.is_empty():
            raise ProviderAssociatedError()

        await self.repo_provider.remove(provider.id)
