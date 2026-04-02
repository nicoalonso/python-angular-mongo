from src.domain.customer import Customer, CustomerRepository
from src.infrastructure.persistence.pymongo.mapping import CustomerDocument
from .mongo_repository import MongoRepository


class MongoCustomerRepository(MongoRepository[Customer], CustomerRepository):
    """
    Repository for Customer entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["customers"], model=CustomerDocument)

    async def obtain_by_name(self, name: str, surname: str) -> Customer | None:
        return await self._find_one_by({"name": name, "surname": surname})

    async def obtain_by_number(self, number: str) -> Customer | None:
        return await self._find_one_by({"membership.number": number})
