from typing import Optional, Any

from pydantic import BaseModel

from .filter_type import  FilterType
from .value_kind import ValueKind
from .filter_range_interval import FilterRangeInterval
from .filter_field import FilterFieldCollection, FilterField
from .sort_field import SortFieldCollection, SortField
from .. import Collection

FIRST_PAGE = 1
DEFAULT_PAGE_LIMIT = 10
INTERNAL_FIELDS = ['page', 'limit', 'sort']


class ListQuery:
    """
    List query class, parse the query parameters for list operation

    :ivar filters: FilterFieldCollection - The filters to apply to the list
    :ivar sort: SortFieldCollection - The sort fields to apply to the list
    :ivar page: int - The page number to return
    :ivar limit: int - The number of items to return per page
    """
    def __init__(
            self,
            *,
            filters: Optional[FilterFieldCollection] = None,
            sort: Optional[SortFieldCollection] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
    ):
        self.filters: FilterFieldCollection = filters or Collection()
        self.sort: SortFieldCollection = sort or Collection()
        self.page: int = page if page and page >= FIRST_PAGE else FIRST_PAGE
        self.limit: int = limit if limit and limit > 0 else DEFAULT_PAGE_LIMIT

    @classmethod
    def parse(cls, query: BaseModel) -> 'ListQuery':
        """Parse the list query from the payload

        :param query: BaseModel The payload to parse
        :return: The parsed list query
        :rtype: ListQuery
        """
        payload: dict[str, Any] = query.model_dump(exclude_none=True, by_alias=True)

        page = ValueKind.to_int(payload.get('page', FIRST_PAGE))
        limit = ValueKind.to_int(payload.get('limit', DEFAULT_PAGE_LIMIT))

        sort_value = ValueKind.to_string(payload.get('sort', ''))
        sort = cls.parse_sort_key(sort_value)

        filters = cls.parse_filters(payload)

        return cls(filters=filters, sort=sort, page=page, limit=limit)

    @staticmethod
    def parse_filters(payload: dict[str, Any]) -> FilterFieldCollection:
        """Parse the filters from the payload

        :param payload: (dict) The payload to parse
        :return: A Collection of FilterField with the field name, operator and value
        :rtype: FilterFieldCollection
        """
        filters = Collection()

        for name in payload.keys():
            if name in INTERNAL_FIELDS:
                continue

            value = payload[name]
            if value is None or (isinstance(value, str) and not value.strip()):
                continue  # Skip empty filters

            (interval_name, interval) = FilterRangeInterval.check(name)
            if interval == FilterRangeInterval.Empty:
                filters.add(FilterField(name, value))
                continue

            filter_field = filters.find_first(lambda item: item.is_(interval_name))
            if filter_field is None:
                filter_field = FilterField(interval_name, value, type_=FilterType.Range)
                filters.add(filter_field)
            filter_field.range(interval, value)

        return filters

    @staticmethod
    def parse_sort_key(sort_value: str) -> SortFieldCollection:
        """Parse the sort value to get the fields and orders

        :param sort_value: (str) The sort value to parse
        :return: A Collection of SortField with the field name and the sort order
        :rtype: SortFieldCollection
        """
        sort = Collection()
        if not sort_value:
            return sort

        sort_list = ValueKind.to_list(sort_value)
        for item in sort_list:
            if not item.strip():
                continue  # pragma: no cover

            sort.add(SortField.from_string(item.strip()))

        return sort

    def has_filters(self) -> bool:
        """Check if the list query has any filter fields

        :rtype: bool
        """
        return not self.filters.is_empty()

    def add_filter(self, filter_field: FilterField) -> None:
        """Add a filter field collection to the list query

        :param filter_field: (FilterField) The filter field collection to add
        """
        self.filters.add(filter_field)

    def remove_filter(self, filter_name: str) -> None:
        """Remove the filter field collection by name

        :param filter_name: (str) The name of the filter field collection to remove
        """
        filter_field = self.find_filter(filter_name)
        if filter_field:
            self.filters.remove(filter_field)

    def find_filter(self, filter_name: str) -> Optional[FilterField]:
        """Find the filter field collection by name

        :param filter_name: (str) The name of the filter field collection to find
        :return: The filter field collection if found, otherwise None
        :rtype: Optional[FilterField]
        """
        return self.filters.find_first(lambda item: item.is_(filter_name))

    def has_sort(self) -> bool:
        """Check if the list query has any sort fields

        :rtype: bool
        """
        return not self.sort.is_empty()

    def add_short(self, sort_field: SortField) -> None:
        """Add a sort field to the list query

        :param SortField sort_field: The sort field to add
        """
        self.sort.add(sort_field)

    def find_short(self, sort_name: str) -> Optional[SortField]:
        """Find the sort field by name

        :param sort_name: (str) The name of the sort field to find
        :return: The sort field if found, otherwise None
        :rtype: Optional[SortField]
        """
        return self.sort.find_first(lambda item: item.is_(sort_name))

    @property
    def offset(self) -> int:
        """Calculate the offset for pagination

        :rtype: int
        """
        return (self.page - FIRST_PAGE) * self.limit
