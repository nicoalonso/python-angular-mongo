from src.domain.borrow import BorrowRepository, BorrowLineRepository, Borrow, BorrowLineCollection
from src.domain.borrow.exception import BorrowNotFoundError
from src.domain.user import UserRepository
from .borrow_checkin_payload import BorrowCheckinPayload
from ..creator.payload import BorrowLinePayload


class BorrowCheckin:
    """
    Use case for checking in a borrowed item.

    :ivar repo_borrow: Repository for managing borrows.
    :ivar repo_borrow_line: Repository for managing borrow lines.
    :ivar repo_user: Repository for managing users.
    """
    def __init__(
            self,
            repo_borrow: BorrowRepository,
            repo_borrow_line: BorrowLineRepository,
            repo_user: UserRepository,
    ):
        self.repo_borrow = repo_borrow
        self.repo_borrow_line = repo_borrow_line
        self.repo_user = repo_user

    async def dispatch(self, borrow_id: str, payload: BorrowCheckinPayload) -> Borrow:
        """
        Check in a borrowed item based on the provided payload.
        """
        borrow = await self.get_borrow_or_fail(borrow_id)
        lines = await self.repo_borrow_line.obtain_by_borrow(borrow.id)

        await self._checkin_lines(lines, payload.lines)

        count_returned = lines.filter(lambda l: l.returned).count()

        user = self.repo_user.obtain_user()
        borrow.modify(count_returned, user.name)
        await self.repo_borrow.save(borrow)

        return borrow

    async def get_borrow_or_fail(self, borrow_id: str) -> Borrow:
        """
        Retrieve a borrow by its ID or raise an error if not found.
        :raises BorrowNotFoundError: If the borrow with the given ID is not found.
        """
        borrow = await self.repo_borrow.obtain_by_id(borrow_id)
        if not borrow:
            raise BorrowNotFoundError(borrow_id)

        return borrow

    async def _checkin_lines(
            self,
            lines: BorrowLineCollection,
            payload_lines: list[BorrowLinePayload]
    ) -> None:
        for payload_line in payload_lines:
            if not payload_line.returned:
                continue

            line = lines.find_first(lambda  l: l.id == payload_line.line_id)
            if not line:
                continue

            line.check_in()
            await self.repo_borrow_line.save(line)
