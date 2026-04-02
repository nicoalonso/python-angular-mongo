import re

from datetime import datetime
from enum import Enum

from dateutil.parser import parse

type ValueType = str | bool | int | float | datetime | None


class ValueKind(Enum):
    String = "vk:string"
    Boolean = "vk:boolean"
    Integer = "vk:integer"
    Float = "vk:float"
    Date = "vk:date"

    @classmethod
    def check(cls, value_kind) -> bool:
        """
        Checks if the given value kind is a valid value kind
        :param value_kind:
        :return: boolean
        """
        return value_kind in cls

    def parse(self, value: ValueType) -> ValueType:
        match self:
            case ValueKind.String:
                return self.to_string(value)
            case ValueKind.Boolean:
                return self.to_bool(value)
            case ValueKind.Integer:
                return self.to_int(value)
            case ValueKind.Float:
                return self.to_float(value)
            case ValueKind.Date:
                return self.to_date(value)

    @staticmethod
    def to_string(value: ValueType) -> str:
        if value is None:
            return ''

        return str(value)

    @staticmethod
    def to_bool(value: ValueType) -> bool:
        if isinstance(value, bool):
            return value
        if not isinstance(value, str):
            return bool(value)

        match value.lower():
            case 'true' | '1' | 'yes' | 'y' | 'on':
                return True
            case _:
                return False

    @staticmethod
    def to_int(value: ValueType) -> int:
        try:
            if value is None:
                return 0
            return int(value)
        except ValueError:
            return 0

    @staticmethod
    def to_float(value: ValueType) -> float:
        try:
            if value is None:
                return 0.0
            return float(value)
        except ValueError:
            return 0.0

    @staticmethod
    def to_date(value: ValueType) -> datetime | None:
        try:
            if not value:
                return None

            return parse(value)
        except ValueError:
            return None

    @staticmethod
    def is_short_date(value: str) -> bool:
        return re.match(r'^\d{4}-\d{2}-\d{2}$', value) is not None

    @staticmethod
    def to_list(value: str) -> list:
        values = re.split(r'[,; ]', value)
        values = map(lambda x: x.strip(), values)
        values = filter(lambda x: len(x) > 0, values)
        return list(values)
