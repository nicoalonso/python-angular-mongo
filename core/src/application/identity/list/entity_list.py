from abc import ABC

from typing_extensions import Generic, TypeVar

from src.domain.identity import ListRepository
from src.domain.identity.list import *
from src.application.identity.list.exception import InvalidFilterError, InvalidSortFieldError

T = TypeVar('T')


class EntityList(Generic[T], ABC):
    """
    Base class for entity list

    :ivar repository: (ListRepository[T]) Repository to get the list of entities
    :ivar field_map: (FieldMap) Map of the fields to be used in the list
    """
    entity_mapping = [
        Field('id'),
        Field('createdBy'),
        Field('createdAt', type_=FilterType.Range, kind=ValueKind.Date),
        Field('updatedBy'),
        Field('updatedAt', type_=FilterType.Range, kind=ValueKind.Date)
    ]
    created_field_name = 'createdAt'

    def __init__(self, repository: ListRepository[T], field_map_record: FieldMapRecord):
        self.repository = repository
        self.field_map = FieldMap([
            *self.entity_mapping,
            *field_map_record,
        ])

    async def dispatch(self, query: ListQuery) -> ListResult[T]:
        """
        Get the list of entities based on the query

        :param query: dict - Query to filter the list of entities
        :return: list[T] - List of entities
        """
        self._check_query(query)
        self.handel_filters(query)

        return await self.repository.obtain_by_query(query)

    def _check_query(self, query: ListQuery) -> None:
        """
        Check if the query is valid based on the field map record

        :param query: ListQuery - Query to filter the list of entities
        """
        self._is_valid_filter_or_fail(query)
        self._is_valid_sort_or_fail(query)

    def _is_valid_filter_or_fail(self, query: ListQuery) -> None:
        """
        Check if the filters in the query are valid based on the field map record
        :param query: (ListQuery) Query to filter the list of entities
        """
        if not query.has_filters():
            return

        for filter_field in query.filters:
            if not self.field_map.can_filter(filter_field):
                raise InvalidFilterError(filter_field.alias)

    def _is_valid_sort_or_fail(self, query:ListQuery) -> None:
        """
        Check if the sort fields in the query are valid based on the field map record
        :param query: (ListQuery) Query to filter the list of entities
        """
        if not query.has_sort():
            return

        for sort in query.sort:
            if not self.field_map.can_sort(sort):
                raise InvalidSortFieldError(sort.alias)

    def handel_filters(self, query: ListQuery) -> None:
        """
        Handle the filters in the query

        :param query: ListQuery - Query to filter the list of entities
        """
        if not query.has_sort() and self.field_map.has_field(self.created_field_name):
            # add default sort by createdAt if no sort is provided and the field is available
            date_sort = SortField(self.created_field_name, direction=SortDirection.Descending)
            query.add_short(date_sort)
