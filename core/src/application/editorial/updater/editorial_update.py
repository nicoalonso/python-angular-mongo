from src.domain.common import EnterpriseContact, Address
from src.domain.editorial import EditorialRepository, Editorial
from src.domain.editorial.exception import EditorialNotFoundError
from src.domain.user import UserRepository
from .editorial_update_payload import EditorialUpdatePayload


class EditorialUpdate:
    """
    Use case for updating an editorial.

    :ivar repo_editorial: Repository for editorial data.
    :ivar repo_user: Repository for user data.
    """
    def __init__(self, repo_editorial: EditorialRepository, repo_user: UserRepository):
        self.repo_editorial = repo_editorial
        self.repo_user = repo_user

    async def dispatch(self, editorial_id: str, payload: EditorialUpdatePayload) -> Editorial:
        """Update an editorial with the given id and payload."""
        editorial = await self.repo_editorial.obtain_by_id(editorial_id)
        if not editorial:
            raise EditorialNotFoundError(editorial_id)

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

        editorial.modify(
            name=payload.name,
            comercial_name=payload.comercial_name,
            contact=contact,
            address=address,
            updated_by=user.name,
        )

        await self.repo_editorial.save(editorial)
        return editorial
