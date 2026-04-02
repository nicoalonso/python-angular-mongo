import pytest

from src.application.borrow.list import BorrowList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import BorrowRepositoryStub


class TestBorrowList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_borrow = BorrowRepositoryStub()
        self.lister = BorrowList(self.repo_borrow)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_borrow.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
