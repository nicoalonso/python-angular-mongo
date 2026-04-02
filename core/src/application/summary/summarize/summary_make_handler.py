import logging

from src.domain.bus import Handler
from src.application.summary.creator import SummaryCreatedEvent
from .summary_make import SummaryMake


class SummaryMakeHandler(Handler):
    """
    Handler for SummaryMake use case

    :ivar _summary_make: SummaryMake use case instance
    """
    def __init__(self, summary_make: SummaryMake):
        self._summary_make = summary_make
        self.log = logging.getLogger('uvicorn')

    async def handle(self, event: SummaryCreatedEvent):
        try:
            return await self._summary_make.dispatch(event.summary_id)
        except Exception as e:
            self.log.error(f"Error handling SummaryCreatedEvent for summary ID {event.summary_id}: {e}")
