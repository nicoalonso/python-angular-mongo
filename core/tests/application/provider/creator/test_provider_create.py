import pytest

from src.application.provider.creator import ProviderCreate, ProviderCreatePayload
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub, UserRepositoryStub
from tests.fixtures import Ref, FixturePayload


class TestProviderCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        repo_user = UserRepositoryStub()
        self.creator = ProviderCreate(self.repo_provider, repo_user)

        loader = FixturePayload()
        data = loader.load('provider')
        self.payload = ProviderCreatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_provider.put(Ref.ProviderAmazon)

        with pytest.raises(Exception):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        provider = await self.creator.dispatch(self.payload)

        assert provider.name == self.payload.name
        assert self.repo_provider.stored is not None
