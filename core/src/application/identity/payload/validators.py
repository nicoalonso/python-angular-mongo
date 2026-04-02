from typing import Annotated

from pydantic import EmailStr, BeforeValidator, HttpUrl


def _empty_str_to_none(value: object) -> object:
    if isinstance(value, str) and value.strip() == "":  # pragma: no cover
        return None
    return value


OptionalEmail = Annotated[EmailStr | None, BeforeValidator(_empty_str_to_none)]

OptionalUrl = Annotated[HttpUrl | None, BeforeValidator(_empty_str_to_none)]
