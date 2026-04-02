from src.domain.identity.list import Field, FilterType, ValueKind
from src.domain.sale import Sale, SaleRepository
from src.application.identity.list import EntityList


class SaleList(EntityList[Sale]):
    """
    Sale list use case
    """
    sale_mapping = [
        Field('customer', name='customer.name'),
        Field('date', name='invoice.date', type_=FilterType.Range, kind=ValueKind.Date),
        Field('number'),
    ]

    def __init__(self, repository: SaleRepository):
        super().__init__(repository, self.sale_mapping)
