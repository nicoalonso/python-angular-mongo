from src.application.editorial.creator.editorial_create_payload import EditorialCreatePayload
from src.domain.common import EnterpriseContact, Address
from src.domain.editorial import EditorialRepository, Editorial
from src.domain.editorial.exception import EditorialAlreadyExistsError
from src.domain.user import UserRepository


class EditorialCreate:
    """
    Use case for creating an editorial.

    :ivar repo_editorial: Repository for editorial data access.
    :ivar repo_user: Repository for user data access.
    """
    def __init__(self, repo_editorial: EditorialRepository, repo_user: UserRepository):
        self.repo_editorial = repo_editorial
        self.repo_user = repo_user

    async def dispatch(self, payload: EditorialCreatePayload) -> Editorial:
        """
        Create a new editorial based on the provided payload.

        :param payload: Data required to create a new editorial.
        :return: The created Editorial object.
        """
        await self._check_already_exists(payload)

        user = self.repo_user.obtain_user()
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

        editorial = Editorial.create(
            name=payload.name,
            comercial_name=payload.comercial_name,
            contact=contact,
            address=address,
            created_by=user.name,
        )

        await self.repo_editorial.save(editorial)
        return editorial

    async def _check_already_exists(self, payload: EditorialCreatePayload) -> None:
        """
        Check if an editorial with the same name already exists.
        :param payload: Data required to create a new editorial.
        """
        editorial = await self.repo_editorial.obtain_by_name(payload.name)
        if editorial is not None:
            raise EditorialAlreadyExistsError()
