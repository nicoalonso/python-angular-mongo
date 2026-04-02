from pydantic import BaseModel

from src.application.borrow.creator.payload import BorrowLinePayload


class BorrowCheckinPayload(BaseModel):
    """Payload for checkin a borrow."""
    lines: list[BorrowLinePayload]
