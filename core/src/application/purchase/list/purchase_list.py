from src.application.identity.list import EntityList
from src.domain.identity.list import Field, FilterType, ValueKind
from src.domain.purchase import PurchaseRepository, Purchase


class PurchaseList(EntityList[Purchase]):
    """
    Purchase list use case
    """
    purchase_mapping = [
        Field('provider', name='provider.name'),
        Field('purchaseAt', type_=FilterType.Range, kind=ValueKind.Date),
        Field('invoiceNumber', name='invoice-number'),
    ]

    def __init__(self, repository: PurchaseRepository):
        super().__init__(repository, self.purchase_mapping)
