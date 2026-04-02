from src.domain.common import EnterpriseContact, Address
from src.domain.provider import ProviderRepository, Provider
from src.domain.provider.exception import ProviderAlreadyExistsError
from src.domain.user import UserRepository
from .provider_create_payload import ProviderCreatePayload


class ProviderCreate:
    """
    Use case for creating a provider.

    :ivar repo_provider: Repository for provider data access.
    :ivar repo_user: Repository for user data access.
    """
    def __init__(
            self,
            repo_provider: ProviderRepository,
            repo_user: UserRepository,
    ):
        self.repo_provider = repo_provider
        self.repo_user = repo_user

    async def dispatch(self, payload: ProviderCreatePayload) -> Provider:
        """
        Create a new provider based on the provided payload.
        :param payload: Data required to create a new provider.
        :return: The created Provider object.
        """
        await self._check_already_exists(payload)

        contact = EnterpriseContact(
            email=payload.contact.email or "",
            website=str(payload.contact.website or ""),
            phone1=payload.contact.phone1,
            phone2=payload.contact.phone2,
        )
        address = Address(
            street=payload.address.street,
            postal_code=payload.address.postal_code,
            city=payload.address.city,
            province=payload.address.province,
            country=payload.address.country,
        )
        user = self.repo_user.obtain_user()

        provider = Provider.create(
            name=payload.name,
            comercial_name=payload.comercial_name,
            contact=contact,
            address=address,
            vat_number=payload.vat_number,
            created_by=user.name,
        )

        await self.repo_provider.save(provider)
        return provider

    async def _check_already_exists(self, payload: ProviderCreatePayload) -> None:
        """Check if a provider with the same name already exists."""
        provider = await self.repo_provider.obtain_by_name(payload.name)
        if provider is not None:
            raise ProviderAlreadyExistsError()
