from enum import Enum


class MotherMapping(Enum):
    """Enum class for mapping mother data types to their corresponding Python types."""
    NONE = 'mm:none'
    ARRAY = 'mm:array'
    DATE = 'mm:date'
    REQUIRED = 'mm:required'
    MOTHER = 'mm:mother'
