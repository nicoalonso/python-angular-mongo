from datetime import datetime, timedelta

import pytest

from src.domain.book import BookDetail
from src.domain.book.exception import InvalidIsbnError, InvalidPublishedDateError


class TestBookDetail:
    def test_should_fail_when_invalid_isbn(self):
        with pytest.raises(InvalidIsbnError) as exc:
            BookDetail.create(
                edition="First Edition",
                isbn="",
                language="English",
                published_at=datetime.now(),
                pages=100
            )

        assert str(exc.value) == 'The ISBN is invalid'

    def test_should_fail_when_invalid_date(self):
        published_at = datetime.now() + timedelta(days=2)

        with pytest.raises(InvalidPublishedDateError) as exc:
            BookDetail.create(
                edition="First Edition",
                isbn="978-1234567890",
                language="English",
                published_at=published_at,
                pages=100
            )

        assert str(exc.value) == 'Published date cannot be in the future.'

    def test_should_create_book_detail(self):
        published_at = datetime.now() - timedelta(days=30)

        detail = BookDetail.create(
            edition="First Edition",
            isbn="978-1234567890",
            language="English",
            published_at=published_at,
            pages=100
        )

        assert detail.edition == "First Edition"
        assert detail.isbn == "978-1234567890"
        assert detail.language == "English"
        assert detail.published_at == published_at
        assert detail.pages == 100
