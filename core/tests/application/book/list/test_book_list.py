import pytest

from src.application.book.list import BookList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import BookRepositoryStub


class TestBookList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repository = BookRepositoryStub()
        self.lister = BookList(self.repository)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repository.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
