from src.domain.identity.exception import BadRequestError


class SaleLinesEmptyError(BadRequestError):
    def __init__(self):
        super().__init__('The sale invoice must have at least one line.')
