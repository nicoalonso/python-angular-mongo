from src.domain.identity.list import Pagination


class TestPagination:
    def test_should_run_when_create(self):
        pagination = Pagination()

        assert pagination.total == 0
        assert pagination.page == 1
        assert pagination.rows_per_page == 10
        assert pagination.total_pages == 0

    def test_should_run_when_is_valid(self):
        pagination = Pagination(total=100, page=2, rows_per_page=10)

        assert pagination.total == 100
        assert pagination.page == 2
        assert pagination.rows_per_page == 10
        assert pagination.total_pages == 10
