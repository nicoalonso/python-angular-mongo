from datetime import datetime
import logging

from src.domain.borrow import BorrowRepository, BorrowLineRepository, Borrow

# This value should be retrieved from admin config
PENALTY_VALUE = 5.0


class BorrowPenalty:
    """
    Use case for calculate penalties for a borrow.

    :ivar repo_borrow: Repository for borrows
    :ivar repo_borrow_line: Repository for borrow lines
    :ivar log: Logger for the class
    """
    def __init__(
            self,
            repo_borrow: BorrowRepository,
            repo_borrow_line: BorrowLineRepository,
    ):
        self.repo_borrow = repo_borrow
        self.repo_borrow_line = repo_borrow_line
        self.log = logging.getLogger('uvicorn')

    async def dispatch(self) -> int:
        """Calculate penalties for all borrows."""
        self.log.info('Start borrow penalty process')
        penalty_borrow_count = 0

        borrows = await self.repo_borrow.obtain_by_overdue()
        self.log.info(f'Found {len(borrows)} overdue borrows')

        for borrow in borrows:
            if await self._manage_borrow(borrow):
                penalty_borrow_count += 1

        self.log.info(f'Borrow penalty process completed. Total penalized borrows: {penalty_borrow_count}')
        return penalty_borrow_count

    async def _manage_borrow(self, borrow: Borrow) -> bool:
        """Calculate and apply penalties for a single borrow."""
        self.log.info(f'Processing borrow ID: {borrow.id}')
        borrow_lines = await self.repo_borrow_line.obtain_by_borrow(borrow.id)
        pending_books = borrow_lines.filter(lambda bl: bl.returned is False)
        self.log.info(f'Borrow ID {borrow.id} has {len(pending_books)} pending books')

        if pending_books.is_empty():
            self.log.info(f'Borrow ID {borrow.id} has no pending books. No penalty applied.')
            return False

        due_date = datetime.now()
        amount = self._calculate_penalty(borrow, due_date)
        borrow.penalize(amount)
        self.log.info(f'Borrow ID {borrow.id} penalized with amount: {amount}')

        for line in pending_books:
            line.penalize(amount)
            await self.repo_borrow_line.save(line)

        await self.repo_borrow.save(borrow)
        return True

    def _calculate_penalty(self, borrow: Borrow, due_date: datetime) -> float:
        """Calculate the penalty amount based on the borrow and due date."""
        diff = (due_date - borrow.due_date).days
        weeks = diff // 7
        self.log.info(f'Borrow ID {borrow.id} is overdue by {diff} days, which is {weeks} weeks')

        return PENALTY_VALUE + max(0, weeks * PENALTY_VALUE)
