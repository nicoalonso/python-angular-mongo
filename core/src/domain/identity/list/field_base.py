from .field import Field


class FieldBase:
    """
    A field base represents a column in a list. It has a name and an alias.

    :ivar name: (str) The name of the field.
    :ivar alias: (str) The alias of the field, which is used for display purposes.
    """
    def __init__(self, name: str):
        self.name = name
        self.alias = name

    def mapping(self, field: Field) -> None:
        """Map the field base to a field

        :param field: (Field) The field to map to
        """
        self.name = field.field_name

    def is_(self, name: str) -> bool:
        """Check if the field base is the same as the field

        :param name: (str) The field to check against

        :rtype: bool
        """
        return self.name == name
