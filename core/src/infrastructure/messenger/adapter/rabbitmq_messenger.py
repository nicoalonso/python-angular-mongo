import logging
from typing import Callable

from pika import BlockingConnection, URLParameters

from src.domain.bus import MessengerAdapter


class RabbitMQMessenger(MessengerAdapter):
    """
    RabbitMQ implementation of the MessengerAdapter for sending messages to RabbitMQ.

    :ivar dsn: str - RabbitMQ DSN
    :ivar exchange: str - RabbitMQ Exchange
    :ivar queue: str - RabbitMQ queue
    :ivar log: logging.Logger - Logger instance for logging purposes

    :ivar _connection: BlockingConnection - RabbitMQ connection instance
    :ivar _channel: BlockingChannel - RabbitMQ channel instance
    :ivar _messenger_callback: Callable - Messenger callback function for consuming messages
    """
    def __init__(self, dsn: str, exchange: str, queue: str):
        self.dsn = dsn
        self.exchange = exchange
        self.queue = queue
        self.log = logging.getLogger('uvicorn')

        self._connection = None
        self._channel = None
        self._messenger_callback = None

    def consume(self, callback: Callable) -> None:
        """Starts consuming messages from the RabbitMQ queue using the provided callback."""
        self.connect()

        self._messenger_callback = callback
        self._channel.basic_consume(queue=self.queue,
                                    auto_ack=True,
                                    on_message_callback=self.callback)
        self.log.info('RabbitMQ: Waiting for messages')
        self._channel.start_consuming()

    def callback(self, _ch, _method, _properties, body) -> None:
        """Internal callback function for RabbitMQ message consumption."""
        self._messenger_callback(body)

    def send(self, message: bytes, route: str) -> None:
        """Sends a message to the RabbitMQ exchange with the specified routing key."""
        self.connect()

        self.log.info(f'Messenger: Sending message to RabbitMQ with route: {route}')
        self._channel.basic_publish(exchange=self.exchange, routing_key=route, body=message)

        self.close()

    def connect(self) -> None:
        """Establishes a connection to RabbitMQ and sets up the channel and queue."""
        self.log.info('Messenger: Connecting to RabbitMQ')
        self._connection = BlockingConnection(URLParameters(self.dsn))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue, durable=True)

    def close(self) -> None:
        """Closes the RabbitMQ connection."""
        if self._connection and self._connection.is_open:
            self._connection.close()
            self._channel = None
            self._connection = None
            self.log.info('Messenger: RabbitMQ connection closed')
