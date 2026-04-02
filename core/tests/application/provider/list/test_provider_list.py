import pytest

from src.application.provider.list import ProviderList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub


class TestProviderList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        self.lister = ProviderList(self.repo_provider)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_provider.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
