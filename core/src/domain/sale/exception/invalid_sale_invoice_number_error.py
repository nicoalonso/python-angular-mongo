from src.domain.identity.exception import BadRequestError


class InvalidSaleInvoiceNumberError(BadRequestError):
    def __init__(self, message: str = 'The sale invoice number is required.'):
        super().__init__(message)
