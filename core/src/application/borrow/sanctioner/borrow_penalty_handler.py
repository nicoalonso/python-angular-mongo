import logging

from src.domain.bus import Handler
from .borrow_penalty import BorrowPenalty
from .borrow_penalty_event import BorrowPenaltyEvent


class BorrowPenaltyHandler(Handler):
    """
    Handler for processing borrow penalties.
    """
    def __init__(self, penalty: BorrowPenalty):
        self.penalty = penalty
        self.log = logging.getLogger('uvicorn')

    async def handle(self, event: BorrowPenaltyEvent):
        try:
            await self.penalty.dispatch()
        except Exception as e:
            self.log.error(f"Error processing borrow penalty: {e}")
