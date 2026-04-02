from src.domain.common import EnterpriseContact, Address
from src.domain.provider import ProviderRepository, Provider
from src.domain.provider.exception import ProviderNotFoundError
from src.domain.user import UserRepository
from .provider_update_payload import ProviderUpdatePayload


class ProviderUpdate:
    """
    Use case for updating a provider.
    """
    def __init__(
            self,
            repo_provider: ProviderRepository,
            repo_user: UserRepository,
    ):
        self.repo_provider = repo_provider
        self.repo_user = repo_user

    async def dispatch(self, provider_id: str, payload: ProviderUpdatePayload) -> Provider:
        """Update a provider with the given id and payload."""
        provider = await self.repo_provider.obtain_by_id(provider_id)
        if not provider:
            raise ProviderNotFoundError(provider_id)

        contact = EnterpriseContact(
            email=payload.contact.email or "",
            website=str(payload.contact.website or ""),
            phone1=payload.contact.phone1,
            phone2=payload.contact.phone2,
        )
        user = self.repo_user.obtain_user()
        address = Address(
            street=payload.address.street,
            postal_code=payload.address.postal_code,
            city=payload.address.city,
            province=payload.address.province,
            country=payload.address.country,
        )

        provider.modify(
            name=payload.name,
            comercial_name=payload.comercial_name,
            contact=contact,
            address=address,
            vat_number=payload.vat_number,
            updated_by=user.name,
        )

        await self.repo_provider.save(provider)
        return provider
