import pytest

from src.application.borrow.creator import BorrowCreate, BorrowCreatePayload
from src.domain.book.exception import BookNotFoundError
from src.domain.borrow.exception import BorrowLinesEmptyError
from src.domain.customer.exception import CustomerNotFoundError
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestBorrowCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.loader = FixturePayload()
        self.repo_customer = CustomerRepositoryStub()
        self.repo_borrow = BorrowRepositoryStub(repo_customer=self.repo_customer)
        self.repo_book = BookRepositoryStub()
        self.repo_borrow_line = BorrowLineRepositoryStub(
            repo_borrow=self.repo_borrow,
            repo_book=self.repo_book,
        )
        repo_sequence = SequenceNumberRepositoryStub()
        repo_user = UserRepositoryStub()

        self.creator = BorrowCreate(
            repo_borrow=self.repo_borrow,
            repo_borrow_line=self.repo_borrow_line,
            repo_customer=self.repo_customer,
            repo_book=self.repo_book,
            repo_sequence_number=repo_sequence,
            repo_user=repo_user,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_empty_lines(self):
        data = self.loader.override(lines=[]).load('borrow-create')
        payload = BorrowCreatePayload(**data)

        with pytest.raises(BorrowLinesEmptyError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_book_not_found(self):
        data = self.loader.load('borrow-create')
        payload = BorrowCreatePayload(**data)

        with pytest.raises(BookNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_customer_not_found(self):
        self.repo_book.put(Ref.BookDonQuijote)

        data = self.loader.load('borrow-create')
        payload = BorrowCreatePayload(**data)

        with pytest.raises(CustomerNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        self.repo_book.put(Ref.BookDonQuijote)
        self.repo_customer.put(Ref.CustomerJohnDoe)

        data = self.loader.load('borrow-create')
        payload = BorrowCreatePayload(**data)

        borrow = await self.creator.dispatch(payload)

        assert borrow.number == 'P-00002'
        assert self.repo_borrow is not None
        assert self.repo_borrow_line is not None
