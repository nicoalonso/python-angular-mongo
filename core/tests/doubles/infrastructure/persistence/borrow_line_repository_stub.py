from typing import Optional

from src.domain.borrow import BorrowLine, BorrowLineRepository, BorrowLineCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import BorrowLineMother
from .entity_repository_stub import EntityRepositoryStub
from .borrow_repository_stub import BorrowRepositoryStub
from .book_repository_stub import BookRepositoryStub


class BorrowLineRepositoryStub(EntityRepositoryStub[BorrowLine], BorrowLineRepository):
    """
    Stub implementation of the BorrowLineRepository for testing purposes.
    """

    def __init__(
            self,
            *,
            repo_borrow: Optional[BorrowRepositoryStub] = None,
            repo_book: Optional[BookRepositoryStub] = None,
    ):
        self.repo_borrow = repo_borrow
        self.repo_book = repo_book

        super().__init__()

    async def obtain_by_borrow(self, borrow_id: str) -> BorrowLineCollection:
        self.query_filter = borrow_id
        self._throw_error()
        return self.list

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> BorrowLineCollection:
        self.query_filter = (book_id, limit)
        self._throw_error()
        return self.list

    async def obtain_active_by_book(self, book_id: str) -> BorrowLineCollection:
        self.query_filter = book_id
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        borrow_john_doe = None
        book_romeo_and_juliet = None
        book_don_quixote = None

        if self.repo_borrow:
            borrow_john_doe = self.repo_borrow.get(Ref.BorrowJohnDoe)

        if self.repo_book:
            book_romeo_and_juliet = self.repo_book.get(Ref.BookRomeoAndJuliet)
            book_don_quixote = self.repo_book.get(Ref.BookDonQuijote)

        borrow_line_john_doe_romeo = BorrowLineMother.romeo_and_juliet(borrow=borrow_john_doe, book=book_romeo_and_juliet)
        self.add_fixture(Ref.BorrowLineJohnRomeoAndJuliet, borrow_line_john_doe_romeo)

        borrow_line_john_doe_don_quixote = BorrowLineMother.don_quijote(borrow=borrow_john_doe, book=book_don_quixote)
        self.add_fixture(Ref.BorrowLineJohnQuijote, borrow_line_john_doe_don_quixote)
