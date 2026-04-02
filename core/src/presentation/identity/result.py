from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pytz import timezone
from typing_extensions import TypeVar, Generic


T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    data: T


def format_date(date: Optional[datetime]) -> Optional[str]:  # pragma: no cover
    if not date:
        return None

    if not date.tzinfo:
        tz = timezone('Europe/Madrid')
        date = date.astimezone(tz)

    return date.isoformat('T', 'seconds')

def format_short_date(date: Optional[datetime]) -> Optional[str]:  # pragma: no cover
    if not date:
        return None

    return date.strftime('%Y-%m-%d')
