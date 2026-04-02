from src.domain.bus import DomainEvent, DomainRoute


class BorrowPenaltyEvent(DomainEvent):
    """
    Event representing a borrow penalty.
    """
    def __init__(self):
        super().__init__('borrow.penalty', 'borrow', DomainRoute.LIBRARY)
