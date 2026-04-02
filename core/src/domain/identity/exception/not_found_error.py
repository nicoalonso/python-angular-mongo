from typing import Optional


class NotFoundError(Exception):
    def __init__(self, message: Optional[str] = None):
        super().__init__(message if message else 'Object not found')
