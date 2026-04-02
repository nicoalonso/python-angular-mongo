from typing import Optional

from .field import Field
from .field_base import FieldBase
from .. import Collection

type FieldMapRecord = list[Field]


class FieldMap:
    """
    A field map is a mapping of field names to their corresponding Field objects.
    It is used to define the fields that are available in a list and how they should be displayed.

    :ivar fields: (Collection[Field]) A list of Field objects that define the fields in the list.

    :param fields: (FieldMapRecord) A list of Field objects that define the fields in the list.
    """
    def __init__(self, fields: FieldMapRecord):
        self.fields: Collection[Field] = Collection(fields)

    def has_field(self, alias: str) -> bool:
        """
        Checks if the field map has a field with the given alias.

        :param alias: The alias of the field to check for.
        :return: True if the field map has a field with the given alias, False otherwise.
        """
        return self.fields.exists(lambda field: field.alias == alias)

    def can_select(self, field: FieldBase) -> bool:
        """
        Checks if the field can be selected in the list.

        :param field: The field to check for.
        :return: True if the field can be selected in the list, False otherwise.
        """
        field_map = self._get_field(field)
        return field_map.options.can_select if field_map else False

    def can_filter(self, field: FieldBase) -> bool:
        """
        Checks if the field can be filtered in the list.

        :param field: The field to check for.
        :return: True if the field can be filtered in the list, False otherwise.
        """
        field_map = self._get_field(field)
        return field_map.options.can_filter if field_map else False

    def can_sort(self, field: FieldBase) -> bool:
        """
        Checks if the field can be sorted in the list.

        :param field: The field to check for.
        :return: True if the field can be sorted in the list, False otherwise.
        """
        field_map = self._get_field(field)
        return field_map.options.can_sort if field_map else False

    def _get_field(self, field: FieldBase) -> Optional[Field]:
        """
        Gets the Field object for the given field.

        :param field: The field to get the Field object for.
        :return: The Field object for the given field.
        """
        found = self.fields.find_first(lambda f: f.alias == field.alias)
        if not found:
            return None

        field.mapping(found)
        return found
