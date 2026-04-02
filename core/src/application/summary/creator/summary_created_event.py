from src.domain.bus import DomainEvent, DomainRoute


class SummaryCreatedEvent(DomainEvent):
    """
    Event triggered when a summary is created.
    """
    def __init__(self, summary_id: str):
        super().__init__('summary.created', 'summary', DomainRoute.LIBRARY)
        self.summary_id = summary_id
