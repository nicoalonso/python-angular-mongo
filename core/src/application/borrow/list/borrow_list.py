from src.application.identity.list import EntityList
from src.domain.borrow import Borrow, BorrowRepository
from src.domain.identity.list import Field, FilterType, ValueKind, FieldOption


class BorrowList(EntityList[Borrow]):
    """
    Borrow list use case
    """
    borrow_mapping = [
        Field('customerId', name='customer.id'),
        Field('customer', name='customer.name'),
        Field('customerNumber', name='customer.number'),
        Field('number'),
        Field('borrowDate', type_=FilterType.Range, kind=ValueKind.Date),
        Field('dueDate', type_=FilterType.Range, kind=ValueKind.Date),
        Field('totalBooks', options=[FieldOption.NoFilter]),
        Field('returned', type_=FilterType.Match, kind=ValueKind.Boolean),
        Field('penalty', type_=FilterType.Match, kind=ValueKind.Boolean),
    ]

    def __init__(self, repository: BorrowRepository):
        super().__init__(repository, self.borrow_mapping)
