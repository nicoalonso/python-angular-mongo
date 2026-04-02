from typing import Optional

import pytest

from src.application.author.list import AuthorList, AuthorQueryPayload
from src.application.identity.list.exception import InvalidFilterError, InvalidSortFieldError
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import AuthorRepositoryStub


class DummyAuthorPayload(AuthorQueryPayload):
    dummy: Optional[str] = None


class TestAuthorList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        self.lister = AuthorList(self.repo_author)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_author.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False

    @pytest.mark.asyncio
    async def test_fail_when_invalid_filter(self):
        payload = DummyAuthorPayload(dummy="value")
        query = ListQuery.parse(payload)

        with pytest.raises(InvalidFilterError):
            await self.lister.dispatch(query)

    @pytest.mark.asyncio
    async def test_fail_when_invalid_sort_field(self):
        payload = DummyAuthorPayload(sort='dummy')
        query = ListQuery.parse(payload)

        with pytest.raises(InvalidSortFieldError):
            await self.lister.dispatch(query)

    @pytest.mark.asyncio
    async def test_run_when_empty(self):
        payload = DummyAuthorPayload(name='Nonexistent Author', sort='-createdAt')
        query = ListQuery.parse(payload)

        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is True
