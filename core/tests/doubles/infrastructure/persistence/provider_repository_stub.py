from src.domain.provider import Provider, ProviderRepository
from tests.fixtures import Ref
from tests.fixtures.mothers import ProviderMother
from .entity_repository_stub import EntityRepositoryStub


class ProviderRepositoryStub(EntityRepositoryStub[Provider], ProviderRepository):
    """
    A stub for the ProviderRepository interface used in tests.
    """

    async def obtain_by_name(self, name: str) -> Provider | None:
        self.query_filter = name
        return self.read

    def make_fixtures(self) -> None:
        amazon = ProviderMother.amazon()
        self.add_fixture(Ref.ProviderAmazon, amazon)

        best_buy = ProviderMother.best_buy()
        self.add_fixture(Ref.ProviderBestBuy, best_buy)
