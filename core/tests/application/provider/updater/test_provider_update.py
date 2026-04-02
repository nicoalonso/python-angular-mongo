import pytest

from src.application.provider.updater import ProviderUpdate, ProviderUpdatePayload
from src.domain.provider.exception import ProviderNotFoundError
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub, UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestProviderUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        repo_user = UserRepositoryStub()
        self.updater = ProviderUpdate(self.repo_provider, repo_user)

        loader = FixturePayload()
        data = loader.load('provider')
        self.payload = ProviderUpdatePayload(**data)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(ProviderNotFoundError) as exc:
            await self.updater.dispatch('non-existing-id', self.payload)

        assert str(exc.value) == 'Provider with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_success(self):
        provider = self.repo_provider.put(Ref.ProviderAmazon)

        await self.updater.dispatch(provider.id, self.payload)

        assert self.repo_provider.stored is not None
