import pytest

from src.application.author.eraser import AuthorDelete, AuthorBookAssociatedError
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub, BookRepositoryStub
from tests.fixtures import Ref


class TestAuthorDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        self.repo_book = BookRepositoryStub(repo_author=self.repo_author)
        self.eraser = AuthorDelete(self.repo_author, self.repo_book)

    @pytest.mark.asyncio
    async def test_fail_when_not_found(self):
        with pytest.raises(Exception) as exc:
            await self.eraser.dispatch('non-existing-id')

        assert str(exc.value) == 'Author with ID non-existing-id not found.'

    @pytest.mark.asyncio
    async def test_fail_when_book_associated(self):
        author = self.repo_author.put(Ref.AuthorShakespeare)
        self.repo_book.attach(Ref.BookRomeoAndJuliet)

        with pytest.raises(AuthorBookAssociatedError) as exc:
            await self.eraser.dispatch(author.id)

        assert str(exc.value) == f"Author with ID '{author.id}' is associated with a book and cannot be deleted."

    @pytest.mark.asyncio
    async def test_success(self):
        author = self.repo_author.put(Ref.AuthorShakespeare)

        await self.eraser.dispatch(author.id)

        assert self.repo_author.removed is not None
