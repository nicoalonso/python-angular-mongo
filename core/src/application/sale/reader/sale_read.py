from src.domain.sale import SaleRepository, SaleLineRepository
from src.domain.sale.exception import SaleNotFoundError
from .sale_decorator import SaleDecorator


class SaleRead:
    """
    Use case for reading a Sale.

    :ivar repo_sale: Repository for managing Sale entities.
    :ivar repo_sale_line: Repository for managing SaleLine entities.
    """
    def __init__(
            self,
            repo_sale: SaleRepository,
            repo_sale_line: SaleLineRepository,
    ):
        self.repo_sale = repo_sale
        self.repo_sale_line = repo_sale_line

    async def dispatch(self, sale_id: str) -> SaleDecorator:
        """
        Retrieves a Sale by its ID.

        :param sale_id: The ID of the Sale to retrieve.
        :return: A decorated sale object containing the Sale and its associated lines.
        :raises SaleNotFoundError: If no Sale with the given ID is found.
        """
        sale = await self.repo_sale.obtain_by_id(sale_id)
        if not sale:
            raise SaleNotFoundError(sale_id)

        lines = await self.repo_sale_line.obtain_by_sale(sale.id)

        return SaleDecorator(sale, lines)
