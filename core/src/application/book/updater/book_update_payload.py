from src.application.book.creator import BookCreatePayload


class BookUpdatePayload(BookCreatePayload):
    """
    Payload for updating a book. Inherits from BookCreatePayload to reuse the same fields.
    """
    pass
