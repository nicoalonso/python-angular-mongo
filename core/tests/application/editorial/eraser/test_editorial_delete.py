import pytest

from src.application.editorial.eraser import EditorialDelete, EditorialBookAssociatedError
from src.domain.editorial.exception import EditorialNotFoundError
from tests.doubles.infrastructure.persistence import EditorialRepositoryStub, BookRepositoryStub
from tests.fixtures import Ref


class TestEditorialDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_editorial = EditorialRepositoryStub()
        self.repo_book = BookRepositoryStub()
        self.eraser = EditorialDelete(self.repo_editorial, self.repo_book)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(EditorialNotFoundError) as exc:
            await self.eraser.dispatch('non-existing-id')

        assert str(exc.value) == 'Editorial with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_fail_when_book_related(self):
        editorial = self.repo_editorial.put(Ref.EditorialAnaya)
        self.repo_book.attach(Ref.BookDonQuijote)

        with pytest.raises(EditorialBookAssociatedError) as exc:
            await self.eraser.dispatch('non-existing-id')

        assert str(exc.value) == f'Cannot delete editorial {editorial.id} because it has related books.'

    @pytest.mark.asyncio
    async def test_success(self):
        editorial = self.repo_editorial.put(Ref.EditorialAnaya)

        await self.eraser.dispatch(editorial.id)

        assert self.repo_editorial.removed is not None
