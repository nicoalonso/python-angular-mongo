from .bad_request_error import BadRequestError


class NameEmptyError(BadRequestError):
    """
    Exception raised when a required name field is empty.
    """
    def __init__(self, message: str = "Name is required."):
        super().__init__(message)
