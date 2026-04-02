from src.domain.editorial import Editorial, EditorialRepository
from tests.doubles.infrastructure.persistence.entity_repository_stub import EntityRepositoryStub
from tests.fixtures import Ref
from tests.fixtures.mothers import EditorialMother


class EditorialRepositoryStub(EntityRepositoryStub[Editorial], EditorialRepository):
    """
    A stub for the EditorialRepository interface used in tests.
    """

    async def obtain_by_name(self, name: str) -> Editorial | None:
        self.query_filter = name
        return self.read

    def make_fixtures(self) -> None:
        anaya = EditorialMother.anaya()
        self.add_fixture(Ref.EditorialAnaya, anaya)
