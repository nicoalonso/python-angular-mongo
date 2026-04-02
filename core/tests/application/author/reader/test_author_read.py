import pytest

from src.application.author.reader import AuthorRead
from src.domain.author.exception import AuthorNotFoundError
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub
from tests.fixtures import Ref


class TestAuthorRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        self.reader = AuthorRead(self.repo_author)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(AuthorNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        author = self.repo_author.put(Ref.AuthorShakespeare)

        result = await self.reader.dispatch(author.id)

        assert result is not None
        assert result.id == author.id
