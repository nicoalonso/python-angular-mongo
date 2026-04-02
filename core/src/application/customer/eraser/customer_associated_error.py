from src.domain.identity.exception import BadRequestError


class CustomerAssociatedError(BadRequestError):
    def __init__(self, message: str = 'The customer is associated with one or more sales or borrows.'):
        super().__init__(message)
