from config import Settings
from src.application.book.inventory import BookInventoryHandler, BookInventoryEvent, BookInventory
from src.application.borrow.sanctioner import BorrowPenaltyHandler, BorrowPenalty, BorrowPenaltyEvent
from src.application.summary.creator import SummaryCreatedEvent
from src.application.summary.summarize import SummaryMakeHandler, SummaryMake
from src.infrastructure.bus import InMemoryDomainBus
from src.infrastructure.messenger import InMemoryMessenger
from src.infrastructure.messenger.adapter import RabbitMQMessenger
from src.infrastructure.persistence.pymongo import MongoConnection
from src.infrastructure.persistence.pymongo.repository import *
from src.infrastructure.services.openai import OpenAITextGenerator


class WorkerCommand:
    """
    WorkerCommand is responsible for executing the worker process.

    :ivar settings: Settings
    :ivar messenger: Messenger
    """
    def __init__(self, settings: Settings):
        self.settings: Settings = settings
        self.messenger = None

    async def execute(self):
        """
        Execute the worker command
        """
        await self.manual_wire()
        await self.messenger.consume()

    async def manual_wire(self):
        """
        Manual wire the dependencies for the worker command.
        Worker can not use the FastAPI dependency injection, so we need to wire the dependencies manually.
        The use cases that the worker handle are limited, so we can wire the dependencies manually
        without using a dependency injection framework or library.
        """
        # Database Connection
        mongo = MongoConnection(
            uri=self.settings.database_url,
            db_name=self.settings.database_name,
        )
        await mongo.connect()

        # Repositories
        book_repository = MongoBookRepository(mongo.db)
        purchase_line_repository = MongoPurchaseLineRepository(mongo.db)
        sale_line_repository = MongoSaleLineRepository(mongo.db)
        borrow_repository = MongoBorrowRepository(mongo.db)
        borrow_line_repository = MongoBorrowLineRepository(mongo.db)
        summary_repository = MongoSummaryRepository(mongo.db)

        # Services
        text_generator = OpenAITextGenerator(
            model=self.settings.openai_model,
            api_key=self.settings.openai_api_key,
        )

        # Use cases
        book_inventory = BookInventory(
            repo_book=book_repository,
            repo_purchase_line=purchase_line_repository,
            repo_sale_line=sale_line_repository,
        )

        borrow_penalty = BorrowPenalty(
            repo_borrow=borrow_repository,
            repo_borrow_line=borrow_line_repository,
        )

        summary_make = SummaryMake(
            repo_summary=summary_repository,
            text_generator=text_generator,
        )

        # Handlers
        book_inventory_handler = BookInventoryHandler(book_inventory)
        borrow_penalty_handler = BorrowPenaltyHandler(borrow_penalty)
        summary_make_handler = SummaryMakeHandler(summary_make)

        # Bus
        bus = InMemoryDomainBus()
        bus.register_handler(BookInventoryEvent, book_inventory_handler)
        bus.register_handler(BorrowPenaltyEvent, borrow_penalty_handler)
        bus.register_handler(SummaryCreatedEvent, summary_make_handler)

        # Messenger
        adapter = RabbitMQMessenger(
            dsn=self.settings.rabbitmq_dsn,
            exchange=self.settings.rabbitmq_exchange,
            queue=self.settings.rabbitmq_queue
        )
        self.messenger = InMemoryMessenger(adapter, bus)
