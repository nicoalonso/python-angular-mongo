from src.application.identity.list import EntityList
from src.domain.editorial import Editorial, EditorialRepository
from src.domain.identity.list import Field


class EditorialList(EntityList[Editorial]):
    """
    Editorial list use case
    """
    editorial_mapping = [
        Field('name'),
        Field('comercialName'),
        Field('website', name='contact.website'),
    ]

    def __init__(self, repository: EditorialRepository):
        super().__init__(repository, self.editorial_mapping)
