import asyncio
import json
import logging
from typing import Optional

from src.domain.bus import *
from src.infrastructure.messenger.serializer import *


class InMemoryMessenger(Messenger):
    """
    In-memory implementation of the Messenger for sending messages.

    :ivar bus: DomainBus - event bus
    :ivar log: logging.Logger - logger instance
    :ivar loop: asyncio.AbstractEventLoop - event loop for asynchronous operations
    """
    def __init__(self, adapter: MessengerAdapter, bus: DomainBus):
        super().__init__(adapter)
        self.log = logging.getLogger('uvicorn')
        self.loop = asyncio.get_event_loop()

        # Double binding to ensure the bus has a reference to this messenger
        self.bus = bus
        bus.set_messenger(messenger=self)

        # add serializers
        self.add_serializer('book.inventory', BookInventorySerializer())
        self.add_serializer('borrow.penalty', BorrowPenaltySerializer())
        self.add_serializer('summary.created', SummaryCreatedSerializer())

    async def consume(self) -> None:
        """Start consuming messages through messenger adapter."""
        self.log.info("Start consuming messages")
        await asyncio.to_thread(self.adapter.consume, self.callback)

    def callback(self, body: bytes) -> None:
        """Callback function to process received messages."""
        self.log.info('Messenger: Received message', extra={'body': body})
        message = self.parse_message(body)
        if not message:
            return

        future = asyncio.run_coroutine_threadsafe(
            self.process_message(message),
            self.loop
        )
        future.add_done_callback(self._log_future_error)

    def parse_message(self, body: bytes) -> Optional[dict]:
        """
        Transcode message body in JSON format to dict

        :param body: bytes - message body
        :return: dict
        """
        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            self.log.error('Messenger: Error parsing message', extra={'body': body})
            message = None

        return message

    async def process_message(self, message: dict) -> None:
        """
        Process message.
        Encode message to event and dispatch it to event bus.
        Use serializer to encode message.

        :param message: dict - message
        """
        self.log.info('Messenger: Process message')
        if 'action' not in message:
            self.log.error('Messenger: malformed message', extra={'message': message})
            return

        action = message['action']
        if action not in self.serializers:
            self.log.error('Messenger: serializer not found', extra={'action': action})
            return

        serializer = self.serializers[action]
        event = serializer.decode(message)
        if not event:
            self.log.error('Messenger: error encoding message', extra={'message': message})
            return

        event.change_route(DomainRoute.NONE)  # Change the route for handler to process the event
        await self.bus.dispatch(event)

    def _log_future_error(self, future: asyncio.Future) -> None:
        """Log any exceptions that occur during asynchronous message processing."""
        exc = future.exception()
        if exc:
            self.log.error('Messenger: Error processing message', exc_info=exc)

    def send(self, message: DomainEvent) -> None:
        """Send a message to transport."""
        self.log.info(f'Messenger: Sending message {message.action}')

        if message.action not in self.serializers:
            self.log.error(f'Messenger: No serializer found for message {message.action}')
            return

        serializer = self.serializers[message.action]
        event = serializer.encode(message)
        if not event:
            self.log.error(f'Messenger: Failed to serialize message {message.action}')
            return

        body = self.dumps_message(event)
        if not body:
            return

        try:
            self.adapter.send(body, message.route.value)
        except Exception as e:  # pragma: no cover
            self.log.error(f'Messenger: Error sending message {message.action}', exc_info=e)

    def dumps_message(self, event: dict) -> Optional[bytes]:
        """
        Transcode event to JSON format

        :param event: dict - event
        :return: bytes
        """
        try:
            body = json.dumps(event).encode()
        except Exception as e:  # pragma: no cover
            self.log.error('Messenger: Error parsing message', extra={'event': event}, exc_info=e)
            body = None

        return body
