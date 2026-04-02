import pytest

from src.application.borrow.reader.borrow_read import BorrowRead
from src.domain.borrow.exception import BorrowNotFoundError
from tests.doubles.infrastructure.persistence import BorrowRepositoryStub, BorrowLineRepositoryStub
from tests.fixtures import Ref


class TestBorrowRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_borrow = BorrowRepositoryStub()
        self.repo_borrow_line = BorrowLineRepositoryStub(repo_borrow=self.repo_borrow)
        self.reader = BorrowRead(self.repo_borrow, self.repo_borrow_line)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(BorrowNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        sale = self.repo_borrow.put(Ref.BorrowJohnDoe)
        self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)

        result = await self.reader.dispatch(sale.id)

        assert result.id == sale.id
        assert result.get_lines().count() == 1
