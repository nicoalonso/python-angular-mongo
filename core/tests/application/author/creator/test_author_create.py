import pytest

from src.application.author.creator import AuthorCreate, AuthorCreatePayload
from src.domain.author.exception import AuthorAlreadyExistsError
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub, UserRepositoryStub
from tests.fixtures import Ref, FixturePayload


class TestAuthorCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        loader = FixturePayload()
        self.repo_author = AuthorRepositoryStub()
        repo_user = UserRepositoryStub()
        self.creator = AuthorCreate(self.repo_author, repo_user)

        data = loader.load('author')
        self.payload = AuthorCreatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_author.put(Ref.AuthorShakespeare)

        with pytest.raises(AuthorAlreadyExistsError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        author = await self.creator.dispatch(self.payload)

        assert author.name == self.payload.name
        assert self.repo_author.stored is not None
