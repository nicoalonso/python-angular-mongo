from enum import Enum
from typing import cast


class FilterRangeInterval(Enum):
    Empty = ''
    From = 'from'
    To = 'to'

    @classmethod
    def check(cls, name: str) -> tuple[str, 'FilterRangeInterval']:
        """
        Checks if the given name is a valid filter range interval
        :param name: The name of the filter range interval to check
        :return: [str, FilterRangeInterval] The name of the filter range interval if it is valid, or the corresponding FilterRangeInterval enum value if it is valid
        """
        interval = FilterRangeInterval.Empty
        if name.startswith(FilterRangeInterval.From.value):
            interval = FilterRangeInterval.From
        elif name.startswith(FilterRangeInterval.To.value):
            interval = FilterRangeInterval.To
        else:
            return name, interval

        length = len(cast(str, cast(object, interval.value)))
        name = name[length:]
        name = name[0].lower() + name[1:] if name else name
        return name, interval
