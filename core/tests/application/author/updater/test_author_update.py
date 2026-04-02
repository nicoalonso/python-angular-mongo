import pytest

from src.application.author.updater import AuthorUpdate, AuthorUpdatePayload
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub, UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestAuthorUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        repo_user = UserRepositoryStub()
        self.updater = AuthorUpdate(self.repo_author, repo_user)

        loader = FixturePayload()
        data = loader.load('author')
        self.payload = AuthorUpdatePayload(**data)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(Exception) as exc:
            await self.updater.dispatch('non-existing-id', self.payload)

        assert str(exc.value) == 'Author with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_success(self):
        author = self.repo_author.put(Ref.AuthorCervantes)

        await self.updater.dispatch(author.id, self.payload)

        assert self.repo_author.stored is not None
