from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.book.exception import InvalidIsbnError, InvalidPublishedDateError


@dataclass
class BookDetail:
    edition: str = None
    isbn: str = None
    language: str = None
    published_at: datetime = None
    pages: int = None

    @classmethod
    def create(
            cls,
            edition: str,
            isbn: str,
            language: str,
            published_at: datetime,
            pages: int,
    ) -> "BookDetail":
        BookDetail.check(isbn, published_at)

        return cls(
            edition=edition,
            isbn=isbn,
            language=language,
            published_at=published_at,
            pages=pages
        )

    @staticmethod
    def check(isbn: str, published_at: datetime):
        if not isbn or isbn.strip() == "":
            raise InvalidIsbnError()

        limit = datetime.now() + timedelta(days=1)
        if published_at > limit:
            raise InvalidPublishedDateError()
