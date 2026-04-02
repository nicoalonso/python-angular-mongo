import pytest

from src.application.editorial.list import EditorialList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub


class TestEditorialList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_editorial = EditorialRepositoryStub()
        self.lister = EditorialList(self.repo_editorial)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_editorial.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
