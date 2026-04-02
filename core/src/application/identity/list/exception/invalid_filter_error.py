from src.domain.identity.exception import BadRequestError


class InvalidFilterError(BadRequestError):
    def __init__(self, name: str):
        super().__init__(f"Invalid filter: {name}")
