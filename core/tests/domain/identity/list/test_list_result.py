from src.domain.identity import Collection
from src.domain.identity.list import ListResult
from src.domain.identity.list.pagination import Pagination


class TestListResult:
    def test_should_run_when_empty(self):
        items = Collection()
        result = ListResult(items)

        assert result.items.to_array() == []
        assert result.pagination.total == 0

    def test_should_run_when_create(self):
        items = Collection(['item1', 'item2'])
        pagination = Pagination(200, 10, 20)
        result = ListResult(items, pagination)

        assert result.items.to_array() == ['item1', 'item2']
        assert result.pagination.total == 200
