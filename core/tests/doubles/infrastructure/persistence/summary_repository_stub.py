from src.domain.summary import Summary, SummaryRepository
from tests.fixtures import Ref
from tests.fixtures.mothers import SummaryMother
from .entity_repository_stub import EntityRepositoryStub


class SummaryRepositoryStub(EntityRepositoryStub[Summary], SummaryRepository):
    """
    SummaryRepositoryStub is a stub implementation of the SummaryRepository interface for testing purposes.
    It extends the EntityRepositoryStub to provide basic in-memory storage and retrieval of Summary entities.
    """

    async def obtain_by_url(self, url: str) -> Summary | None:
        return self.read

    def make_fixtures(self) -> None:
        summary_description = SummaryMother.description()
        self.add_fixture(Ref.SummaryDescription, summary_description)

        summary_biography = SummaryMother.biography()
        self.add_fixture(Ref.SummaryBiography, summary_biography)
