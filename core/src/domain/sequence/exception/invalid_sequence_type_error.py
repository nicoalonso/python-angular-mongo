from src.domain.identity.exception import BadRequestError


class InvalidSequenceTypeError(BadRequestError):
    def __init__(self):
        super().__init__(f"Invalid sequence type")
