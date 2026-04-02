from typing import Optional

from src.domain.sequence import SequenceNumberRepository, SequenceType, SequenceNumber


class SequenceNumberRepositoryStub(SequenceNumberRepository):
    """A stub for the SequenceNumberRepository interface used in tests."""

    def __init__(self):
        self._exception: Optional[Exception] = None

    async def obtain_by_type(self, type_: SequenceType) -> SequenceNumber:
        self._throw_error()

        sequence = SequenceNumber.create(type_)
        sequence.next()
        return sequence

    async def next_number(self, type_: SequenceType) -> SequenceNumber:
        self._throw_error()

        sequence = SequenceNumber.create(type_)
        sequence.next()
        return sequence

    def error(self, exception: Exception | str) -> None:
        if isinstance(exception, str):
            exception = Exception(exception)
        self._exception = exception

    def _throw_error(self):
        if self._exception:
            raise self._exception
