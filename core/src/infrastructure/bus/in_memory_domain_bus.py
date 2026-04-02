import logging

from src.domain.bus import *


class InMemoryDomainBus(DomainBus):
    """
    In-memory implementation of the DomainBus for dispatching commands and events.

    :ivar _handlers: A dictionary mapping event types to their respective handlers.
    :ivar _log: A logger instance for logging purposes.
    """

    def __init__(self):
        super().__init__()
        self._handlers: dict[type[DomainEvent], list[Handler]] = {}
        self._log = logging.getLogger('uvicorn')

    async def dispatch(self, event: DomainEvent):
        """Dispatches an event to all registered handlers for its type."""
        self._log.info(f"Dispatching event: {event.__class__.__name__}")

        if event.route != DomainRoute.NONE:
            self._log.info(f"Event {event.__class__.__name__} has route {event.route}, dispatching to messenger")
            self.send(event)
            return

        for handler in self._handlers.get(type(event), []):
            self._log.info(f"Handling event {event.__class__.__name__} with handler {handler.__class__.__name__}")
            await handler.handle(event)

    def register_handler(self, event_type: type[DomainEvent], handler: Handler) -> None:
        """Registers a handler for a specific event type."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []

        self._handlers[event_type].append(handler)
        self._log.info(f"Registered handler {handler.__class__.__name__} for event type {event_type.__name__}")
