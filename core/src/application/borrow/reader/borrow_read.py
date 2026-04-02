from src.application.borrow.reader.borrow_decorator import BorrowDecorator
from src.domain.borrow import BorrowRepository, BorrowLineRepository
from src.domain.borrow.exception import BorrowNotFoundError


class BorrowRead:
    """
    Use case for reading borrow information.

    :ivar repo_borrow: Repository for managing Borrow entities.
    :ivar repo_borrow_line: Repository for managing BorrowLine entities.
    """
    def __init__(
            self,
            repo_borrow: BorrowRepository,
            repo_borrow_line: BorrowLineRepository,
    ):
        self.repo_borrow = repo_borrow
        self.repo_borrow_line = repo_borrow_line

    async def dispatch(self, borrow_id: str) -> BorrowDecorator:
        """
        Retrieves a Borrow by its ID along with its associated lines.

        :param borrow_id: The ID of the Borrow to retrieve.
        :return: A decorated borrow object containing the Borrow and its associated lines.
        :raises BorrowNotFoundError: If no Borrow with the given ID is found.
        """
        borrow = await self.repo_borrow.obtain_by_id(borrow_id)
        if not borrow:
            raise BorrowNotFoundError(borrow_id)

        lines = await self.repo_borrow_line.obtain_by_borrow(borrow.id)

        return BorrowDecorator(borrow, lines)
