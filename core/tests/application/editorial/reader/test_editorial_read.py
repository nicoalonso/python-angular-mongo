import pytest

from src.application.editorial.reader import EditorialRead
from src.domain.editorial.exception import EditorialNotFoundError
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub
from tests.fixtures import Ref


class TestEditorialRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_editorial = EditorialRepositoryStub()
        self.reader = EditorialRead(self.repo_editorial)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(EditorialNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        editorial = self.repo_editorial.put(Ref.EditorialAnaya)

        result = await self.reader.dispatch(editorial.id)

        assert result is not None
        assert result.id == editorial.id
