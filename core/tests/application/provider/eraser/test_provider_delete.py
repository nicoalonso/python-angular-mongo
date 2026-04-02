import pytest

from src.application.provider.eraser import ProviderDelete, ProviderAssociatedError
from src.domain.provider.exception import ProviderNotFoundError
from tests.doubles.infrastructure.persistence import ProviderRepositoryStub, PurchaseRepositoryStub
from tests.fixtures import Ref


class TestProviderDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        self.repo_purchase = PurchaseRepositoryStub(
            repo_provider=self.repo_provider,
        )
        self.eraser = ProviderDelete(self.repo_provider, self.repo_purchase)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(ProviderNotFoundError) as exc:
            await self.eraser.dispatch('non-existing-id')

        assert str(exc.value) == 'Provider with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        provider = self.repo_provider.put(Ref.ProviderAmazon)
        self.repo_purchase.attach(Ref.PurchaseAmazonInv1)

        with pytest.raises(ProviderAssociatedError) as exc:
            await self.eraser.dispatch(provider.id)

        assert str(exc.value) == 'Provider has purchases and cannot be deleted'

    @pytest.mark.asyncio
    async def test_success(self):
        provider = self.repo_provider.put(Ref.ProviderAmazon)

        await self.eraser.dispatch(provider.id)

        assert self.repo_provider.removed is not None
