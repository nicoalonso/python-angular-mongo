from src.domain.author import Author, AuthorRepository
from tests.fixtures import Ref
from tests.fixtures.mothers import AuthorMother
from .entity_repository_stub import EntityRepositoryStub


class AuthorRepositoryStub(EntityRepositoryStub[Author], AuthorRepository):
    """
    A stub for the AuthorRepository interface used in tests.
    """

    async def obtain_by_name(self, name: str) -> Author | None:
        self.query_filter = name
        return self.read

    def make_fixtures(self) -> None:
        shakespeare = AuthorMother.shakespeare()
        self.add_fixture(Ref.AuthorShakespeare, shakespeare)

        cervantes = AuthorMother.cervantes()
        self.add_fixture(Ref.AuthorCervantes, cervantes)
