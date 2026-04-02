from dataclasses import dataclass

from src.domain.author import AuthorDescriptor, Author
from src.domain.editorial import EditorialDescriptor, Editorial
from src.domain.identity import Entity, Collection
from .book_descriptor import BookDescriptor
from .book_detail import BookDetail
from .book_sale import BookSale
from .exception import TitleEmptyError


@dataclass
class Book(Entity):
    """
    Book entity represents a book in the system.

    Attributes:
        title (str): The title of the book.
        description (str): A brief description of the book.
        author (AuthorDescriptor): A descriptor containing information about the book's author.
        editorial (EditorialDescriptor): A descriptor containing information about the book's editorial.
        detail (BookDetail): Detailed information about the book, such as publication date, ISBN, etc.
        sale (BookSale): Information about the book's sale, such as price, discounts, etc.
        stock (int): The number of copies of the book available in stock.
    """
    title: str = None
    description: str = None
    author: AuthorDescriptor = None
    editorial: EditorialDescriptor = None
    detail: BookDetail = None
    sale: BookSale = None
    stock: int = 0

    @classmethod
    def create(
            cls,
            title: str,
            description: str,
            author: Author,
            editorial: Editorial,
            detail: BookDetail,
            sale: BookSale,
            created_by: str,
    ) -> "Book":
        """
        Factory method to create a new Book instance.
        """
        cls.check(title)

        return cls(
            title=title,
            description=description,
            author=author.get_descriptor(),
            editorial=editorial.get_descriptor(),
            detail=detail,
            sale=sale,
            stock=0,
            created_by=created_by,
        )

    def modify(
            self,
            title: str,
            description: str,
            author: Author,
            editorial: Editorial,
            detail: BookDetail,
            sale: BookSale,
            updated_by: str,
    ) -> None:
        """
        Method to modify the book's attributes.
        """
        self.check(self.title)

        self.title = title
        self.description = description
        self.author = author.get_descriptor()
        self.editorial = editorial.get_descriptor()
        self.detail = detail
        self.sale = sale
        self.updated(updated_by)

    @staticmethod
    def check(title: str) -> None:
        """
        Validates the book's title.
        """
        if not title or title.strip() == "":
            raise TitleEmptyError()

    def change_stock(self, stock: int) -> None:
        """
        Changes the stock of the book by a given amount.
        """
        if stock < 0:
            stock = 0
        self.stock = stock

    def get_descriptor(self) -> "BookDescriptor":
        """
        Returns a descriptor for the book.
        """
        return BookDescriptor(
            id=self.id,
            title=self.title,
            isbn=self.detail.isbn,
        )

type BookCollection = Collection[Book]
