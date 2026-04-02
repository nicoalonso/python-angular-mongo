from src.application.identity.list import EntityList
from src.domain.identity.list import Field
from src.domain.provider import Provider, ProviderRepository


class ProviderList(EntityList[Provider]):
    """
    Provider list use case
    """
    provider_mapping = [
        Field('name'),
        Field('comercialName'),
        Field('vatNumber'),
        Field('website', name='contact.website'),
    ]

    def __init__(self, repository: ProviderRepository):
        super().__init__(repository, self.provider_mapping)
