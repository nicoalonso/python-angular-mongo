import pytest

from src.application.editorial.creator import EditorialCreate, EditorialCreatePayload
from src.domain.editorial.exception import EditorialAlreadyExistsError
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub, UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestEditorialCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_editorial = EditorialRepositoryStub()
        repo_user = UserRepositoryStub()
        self.creator = EditorialCreate(self.repo_editorial, repo_user)

        loader = FixturePayload()
        data = loader.load('editorial')
        self.payload = EditorialCreatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_editorial.put(Ref.EditorialAnaya)

        with pytest.raises(EditorialAlreadyExistsError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        editorial = await self.creator.dispatch(self.payload)

        assert editorial.name == self.payload.name
        assert self.repo_editorial.stored is not None
