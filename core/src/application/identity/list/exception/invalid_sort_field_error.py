from src.domain.identity.exception import BadRequestError


class InvalidSortFieldError(BadRequestError):
    def __init__(self, name: str):
        super().__init__(f"Invalid sort field: {name}")
