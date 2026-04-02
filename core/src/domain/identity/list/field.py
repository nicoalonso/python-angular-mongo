from typing import Optional

from .filter_type import FilterType
from .value_kind import ValueKind
from .field_option import FieldOption
from .field_options import FieldOptions


class Field:
    """
    A field represents a mapping for a column in a list.

    :ivar alias (str): The alias of the field, which is used for display purposes.
    :ivar field_name (str): The actual name of the field in the data source.
    :ivar type_ (FilterType): The filter type for the field, if applicable.
    :ivar kind (ValueKind): The value kind for the field, if applicable.
    :ivar options (FieldOptions): The field options for the field, if applicable.

    :param alias: (str) The alias of the field, which is used for display purposes.
    :param name: (str) The actual name of the field in the data source. If not provided, it defaults to the alias.
    :param type_: (FilterType) The filter type for the field, if applicable.
    :param kind: (ValueKind) The value kind for the field, if applicable.
    :param options: (list[FieldOption]) The field options for the field, if applicable.
    """
    def __init__(
            self,
            alias: str,
            *,
            name: Optional[str] = None,
            type_: Optional[FilterType] = None,
            kind: Optional[ValueKind] = None,
            options: Optional[list[FieldOption]] = None,
    ):
        self.alias = alias
        self.field_name = name or alias
        self.type_ = type_ or FilterType.Wildcard
        self.kind = kind or ValueKind.String

        self.options = FieldOptions()
        self.options.add_options(options or [])
