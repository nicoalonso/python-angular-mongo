from src.application.identity.list import EntityList
from src.domain.book import Book
from src.domain.book.book_repository import BookRepository
from src.domain.identity.list import Field, FilterType, ValueKind


class BookList(EntityList[Book]):
    """
    Book list use case
    """
    book_mapping = [
        Field('title'),
        Field('author', name='author.name'),
        Field('editorial', name='editorial.name'),
        Field('isbn', name='detail.isbn'),
        Field('language', name='detail.language'),
        Field('publishedAt', name='detail.publishedAt', type_=FilterType.Range, kind=ValueKind.Date),
        Field('price', name='sale.price', type_=FilterType.Range, kind=ValueKind.Float),
        Field('saleable', name='sale.saleable', type_=FilterType.Match, kind=ValueKind.Boolean),
    ]

    def __init__(self, repository: BookRepository):
        super().__init__(repository, self.book_mapping)
