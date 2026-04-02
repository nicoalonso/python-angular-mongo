from typing import Annotated

from fastapi import Depends, Request
from pymongo.asynchronous.database import AsyncDatabase

from src.domain.author import AuthorRepository
from src.domain.user import UserRepository
from src.infrastructure.persistence.pymongo.repository import *
from src.infrastructure.persistence.session.repository import SessionUserRepository


def get_db(request: Request) -> AsyncDatabase:
    return request.app.state.mongo.db


def get_author_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> AuthorRepository:
    return MongoAuthorRepository(db)


def get_editorial_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoEditorialRepository:
    return MongoEditorialRepository(db)


def get_book_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoBookRepository:
    return MongoBookRepository(db)


def get_provider_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoProviderRepository:
    return MongoProviderRepository(db)


def get_purchase_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoPurchaseRepository:
    return MongoPurchaseRepository(db)


def get_purchase_line_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoPurchaseLineRepository:
    return MongoPurchaseLineRepository(db)


def get_customer_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoCustomerRepository:
    return MongoCustomerRepository(db)


def get_sequence_number_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoSequenceNumberRepository:
    return MongoSequenceNumberRepository(db)


def get_sale_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoSaleRepository:
    return MongoSaleRepository(db)


def get_sale_line_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoSaleLineRepository:
    return MongoSaleLineRepository(db)


def get_borrow_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoBorrowRepository:
    return MongoBorrowRepository(db)


def get_borrow_line_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoBorrowLineRepository:
    return MongoBorrowLineRepository(db)


def get_summary_repository(db: Annotated[AsyncDatabase, Depends(get_db)]) -> MongoSummaryRepository:
    return MongoSummaryRepository(db)


def get_user_repository() -> UserRepository:
    return SessionUserRepository()


__all__ = [
    "get_author_repository",
    "get_editorial_repository",
    "get_book_repository",
    "get_provider_repository",
    "get_purchase_repository",
    "get_purchase_line_repository",
    "get_customer_repository",
    "get_sequence_number_repository",
    "get_sale_repository",
    "get_sale_line_repository",
    "get_user_repository",
    "get_borrow_repository",
    "get_borrow_line_repository",
    "get_summary_repository",
]
