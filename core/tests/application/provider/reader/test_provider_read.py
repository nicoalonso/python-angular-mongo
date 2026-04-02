import pytest

from src.application.provider.reader import ProviderRead
from src.domain.provider.exception import ProviderNotFoundError
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub
from tests.fixtures import Ref


class TestProviderRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        self.reader = ProviderRead(self.repo_provider)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(ProviderNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        provider = self.repo_provider.put(Ref.ProviderAmazon)

        result = await self.reader.dispatch(provider.id)

        assert result is not None
        assert result.id == provider.id
