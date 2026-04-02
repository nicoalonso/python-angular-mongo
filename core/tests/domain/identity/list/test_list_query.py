from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQuery, ListQueryPayload, FilterField, SortDirection, SortField


class DummyPayload(ListQueryPayload):
    test1: Optional[str] = None
    test2: Optional[str] = None
    from_age: Optional[int] = Field(default=None, alias='fromAge')
    to_age: Optional[int] = Field(default=None, alias='toAge')


class TestListQuery:
    def test_should_create(self):
        query = ListQuery()

        assert query.filters.is_empty()
        assert query.sort.is_empty()
        assert query.page == 1
        assert query.limit == 10
        assert query.offset == 0

        assert query.has_filters() is False
        assert query.has_sort() is False

    def test_should_valid_when_parse_with_filters(self):
        payload = DummyPayload(test1='value1', test2='value2')

        query = ListQuery.parse(payload)

        assert query.filters.is_empty() is False
        assert query.filters.count() == 2
        assert query.has_filters() is True

        first_filter = query.filters.first()
        assert first_filter.name == 'test1'
        assert first_filter.value == 'value1'
        assert query.find_filter('test1') == first_filter

    def test_should_not_found_when_filter_not_exists(self):
        payload = DummyPayload(test1='value1')

        query = ListQuery.parse(payload)

        assert query.find_filter('nonexistent') is None

    def test_should_range_filter_when_define_range(self):
        payload = DummyPayload(fromAge=18, toAge=50)

        query = ListQuery.parse(payload)

        assert query.has_filters()
        assert query.filters.count() == 1

        first_filter = query.filters.first()
        assert first_filter.alias == 'age'
        assert first_filter.name == 'age'
        assert first_filter.value.from_ == 18
        assert first_filter.value.to == 50

    def test_should_run_when_empty_values(self):
        payload = DummyPayload(test1='', test2=None)

        query = ListQuery.parse(payload)

        assert query.filters.is_empty() is True
        assert query.has_filters() is False

    def test_should_run_when_add_filter(self):
        query = ListQuery()

        filter_field = FilterField('test', 'value')
        query.add_filter(filter_field)

        assert query.filters.count() == 1
        first_filter = query.filters.first()
        assert first_filter.name == 'test'
        assert first_filter.value == 'value'

    def test_should_run_remove_filter(self):
        payload = DummyPayload(test1='value1', test2='value2')

        query = ListQuery.parse(payload)

        assert query.filters.count() == 2

        query.remove_filter('test1')

        assert query.filters.count() == 1
        first_filter = query.filters.first()
        assert first_filter.name == 'test2'
        assert first_filter.value == 'value2'

    def test_should_fail_when_remove_nonexistent_filter(self):
        payload = DummyPayload(test1='value1')

        query = ListQuery.parse(payload)

        assert query.filters.count() == 1

        query.remove_filter('nonexistent')

        assert query.filters.count() == 1

    def test_should_valid_when_parse_with_sort(self):
        payload = DummyPayload(sort='test1,-test2')

        query = ListQuery.parse(payload)

        assert query.sort.is_empty() is False
        assert query.sort.count() == 2
        assert query.has_sort() is True

        first_sort = query.sort.first()
        assert first_sort.name == 'test1'
        assert first_sort.direction == SortDirection.Ascending
        assert query.find_short('test1') == first_sort

    def test_should_not_found_when_sort_not_exists(self):
        payload = DummyPayload(sort='test1')

        query = ListQuery.parse(payload)

        assert query.find_short('nonexistent') is None

    def test_should_run_when_space_before_field(self):
        payload = DummyPayload(sort=' test1')

        query = ListQuery.parse(payload)

        assert query.sort.is_empty() is False
        assert query.sort.count() == 1
        first_sort = query.sort.first()
        assert first_sort.name == 'test1'
        assert first_sort.direction == SortDirection.Ascending

    def test_should_run_when_add_sort_field(self):
        query = ListQuery()

        sort_field = SortField('test', direction=SortDirection.Descending)
        query.add_short(sort_field)

        assert query.sort.count() == 1
        first_sort = query.sort.first()
        assert first_sort.name == 'test'
        assert first_sort.direction == SortDirection.Descending

    def test_should_run_when_parse_with_pagination(self):
        payload = DummyPayload(page=2, limit=20)

        query = ListQuery.parse(payload)

        assert query.page == 2
        assert query.limit == 20
        assert query.offset == 20
