from src.application.identity.list import EntityList
from src.domain.customer import Customer, CustomerRepository
from src.domain.identity.list import Field, FilterType, ValueKind


class CustomerList(EntityList[Customer]):
    """
    Customer list use case
    """
    customer_mapping = [
        Field('name'),
        Field('surname'),
        Field('number', name='membership.number'),
        Field('active', name='membership.active', type_=FilterType.Match, kind=ValueKind.Boolean),
        Field('city', name='address.city'),
        Field('vatNumber'),
    ]

    def __init__(self, repository: CustomerRepository):
        super().__init__(repository, self.customer_mapping)
