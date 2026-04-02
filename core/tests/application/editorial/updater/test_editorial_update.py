import pytest

from src.application.editorial.updater import EditorialUpdate, EditorialUpdatePayload
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub, UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestEditorialUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_editorial = EditorialRepositoryStub()
        repo_user = UserRepositoryStub()
        self.updater = EditorialUpdate(self.repo_editorial, repo_user)

        loader = FixturePayload()
        data = loader.load('editorial')
        self.payload = EditorialUpdatePayload(**data)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(Exception) as exc:
            await self.updater.dispatch('non-existing-id', self.payload)

        assert str(exc.value) == 'Editorial with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_success(self):
        editorial = self.repo_editorial.put(Ref.EditorialAnaya)

        await self.updater.dispatch(editorial.id, self.payload)

        assert self.repo_editorial.stored is not None

