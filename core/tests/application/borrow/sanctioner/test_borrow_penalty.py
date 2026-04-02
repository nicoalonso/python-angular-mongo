from datetime import datetime, timedelta

import pytest

from src.application.borrow.sanctioner import BorrowPenalty
from tests.doubles.infrastructure.persistence import BorrowRepositoryStub, BorrowLineRepositoryStub
from tests.fixtures import Ref


class TestBorrowPenalty:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_borrow = BorrowRepositoryStub()
        self.repo_borrow_line = BorrowLineRepositoryStub(repo_borrow=self.repo_borrow)
        self.sanctioner = BorrowPenalty(
            repo_borrow=self.repo_borrow,
            repo_borrow_line=self.repo_borrow_line,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_borrow_line_not_found(self):
        borrow = self.repo_borrow.attach(Ref.BorrowJohnDoe)
        borrow.due_date = datetime.now() - timedelta(days=16)

        count = await self.sanctioner.dispatch()

        assert count == 0
        assert self.repo_borrow.stored is None
        assert self.repo_borrow_line.stored is None

    @pytest.mark.asyncio
    async def test_should_run_when_found_penalties(self):
        borrow = self.repo_borrow.attach(Ref.BorrowJohnDoe)
        line = self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)

        borrow.due_date = datetime.now() - timedelta(days=16)

        count = await self.sanctioner.dispatch()

        assert count == 1
        assert borrow.penalty
        assert borrow.penalty_amount == 15.0
        assert line.penalty
        assert line.penalty_amount == 15.0
        assert self.repo_borrow.stored is not None
        assert self.repo_borrow_line.stored is not None
