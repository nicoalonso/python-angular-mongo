from typing import Optional


class BadRequestError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message if message else 'Bad request')
