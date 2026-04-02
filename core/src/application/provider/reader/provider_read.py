from src.domain.provider import ProviderRepository, Provider
from src.domain.provider.exception import ProviderNotFoundError


class ProviderRead:
    """
    Use case for reading provider

    :ivar repo_provider: ProviderRepository
    """
    def __init__(self, repo_provider: ProviderRepository):
        self.repo_provider = repo_provider

    async def dispatch(self, provider_id: str) -> Provider:
        """
        Dispatch the use case to read a provider by its ID.

        :param provider_id: The ID of the provider to read.
        :return: The provider data.
        """
        provider = await self.repo_provider.obtain_by_id(provider_id)
        if not provider:
            raise ProviderNotFoundError(provider_id)

        return provider
