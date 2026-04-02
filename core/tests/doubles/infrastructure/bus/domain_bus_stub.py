from typing import Optional, cast

from src.domain.bus import DomainBus, DomainEvent, Handler
from src.domain.identity import Collection


class DomainBusStub(DomainBus):
    """
    Stub for the DomainBus.
    """
    def __init__(self):
        super().__init__()
        self.events: Collection[DomainEvent] = Collection()
        self.last_event: Optional[DomainEvent] = None
        self._exception: Optional[Exception] = None

    async def dispatch(self, event: DomainEvent):
        self._throw_error()

        self.events.add(event)
        self.last_event = event

    def register_handler(self, event_type: type[DomainEvent], handler: Handler) -> None:
        pass

    def error(self, exception: Exception | str) -> None:
        if isinstance(exception, str):
            exception = Exception(exception)
        self._exception = cast(Exception, exception)

    def _throw_error(self):
        if self._exception:
            raise self._exception


def assert_dispatch(bus: DomainBusStub, expected_event: type[DomainEvent]):
    """
    Asserts that the expected event was dispatched.
    """
    event_exists = bus.events.exists(lambda event: type(event) == expected_event)
    assert event_exists, f"Expected event {expected_event.__name__} was dispatched"
