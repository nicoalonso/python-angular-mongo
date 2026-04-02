import pytest

from src.application.borrow.checkin import BorrowCheckinPayload
from src.application.borrow.checkin.borrow_checkin import BorrowCheckin
from src.domain.borrow.exception import BorrowNotFoundError
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestBorrowCheckin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.loader = FixturePayload()
        self.repo_borrow = BorrowRepositoryStub()
        self.repo_borrow_line = BorrowLineRepositoryStub(
            repo_borrow=self.repo_borrow,
        )
        repo_user = UserRepositoryStub()

        self.creator = BorrowCheckin(
            repo_borrow=self.repo_borrow,
            repo_borrow_line=self.repo_borrow_line,
            repo_user=repo_user,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        data = self.loader.load('borrow-checkin')
        payload = BorrowCheckinPayload(**data)

        with pytest.raises(BorrowNotFoundError):
            await self.creator.dispatch('invalid-id', payload)

    @pytest.mark.asyncio
    async def test_should_checkin_borrow(self):
        self.repo_borrow.put(Ref.BorrowJohnDoe)
        line1 = self.repo_borrow_line.attach(Ref.BorrowLineJohnRomeoAndJuliet)
        line2 = self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)

        data = self.loader.load('borrow-checkin')
        data['lines'][0]['lineId'] = line1.id
        data['lines'][1]['lineId'] = line2.id
        payload = BorrowCheckinPayload(**data)

        borrow = await self.creator.dispatch('121221', payload)

        assert borrow.total_returned_books == 1
        assert self.repo_borrow is not None
        assert self.repo_borrow_line is not None
