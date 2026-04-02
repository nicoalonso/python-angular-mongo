import pytest

from src.domain.book import Book
from src.domain.book.exception import TitleEmptyError
from tests.fixtures.mothers import AuthorMother, EditorialMother, BookDetailMother, BookSaleMother


class TestBook:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.author = AuthorMother.cervantes()
        self.editorial = EditorialMother.anaya()
        self.detail = BookDetailMother.quijote()
        self.sale = BookSaleMother.valid()

    def test_should_fail_when_title_is_empty(self):
        with pytest.raises(TitleEmptyError):
            Book.create(
                title='',
                description='A thrilling adventure story.',
                author=self.author,
                editorial=self.editorial,
                detail=self.detail,
                sale=self.sale,
                created_by='test',
            )

    def test_should_create(self):
        book = Book.create(
            title='Don Quijote de la Mancha',
            description='A thrilling adventure story.',
            author=self.author,
            editorial=self.editorial,
            detail=self.detail,
            sale=self.sale,
            created_by='test',
        )

        assert book.title == 'Don Quijote de la Mancha'
        assert book.description == 'A thrilling adventure story.'
        assert book.author == self.author.get_descriptor()
        assert book.editorial == self.editorial.get_descriptor()
        assert book.detail == self.detail
        assert book.sale == self.sale
        assert book.stock == 0

    def test_should_modify(self):
        book = Book.create(
            title='Don Quijote de la Mancha',
            description='A thrilling adventure story.',
            author=self.author,
            editorial=self.editorial,
            detail=self.detail,
            sale=self.sale,
            created_by='test',
        )

        new_author = AuthorMother.cervantes()
        new_editorial = EditorialMother.anaya()
        new_detail = BookDetailMother.quijote()
        new_sale = BookSaleMother.valid()

        book.modify(
            title='Don Quijote de la Mancha - Updated',
            description='An updated thrilling adventure story.',
            author=new_author,
            editorial=new_editorial,
            detail=new_detail,
            sale=new_sale,
            updated_by='test',
        )

        assert book.title == 'Don Quijote de la Mancha - Updated'
        assert book.description == 'An updated thrilling adventure story.'
        assert book.author == new_author.get_descriptor()
        assert book.editorial == new_editorial.get_descriptor()
        assert book.detail == new_detail
        assert book.sale == new_sale

    def test_should_run_when_get_descriptor(self):
        book = Book.create(
            title='Don Quijote de la Mancha',
            description='A thrilling adventure story.',
            author=self.author,
            editorial=self.editorial,
            detail=self.detail,
            sale=self.sale,
            created_by='test',
        )

        descriptor = book.get_descriptor()

        assert descriptor.id == book.id
        assert descriptor.title == 'Don Quijote de la Mancha'
        assert descriptor.isbn == self.detail.isbn

    def test_should_run_change_stock(self):
        book = Book.create(
            title='Don Quijote de la Mancha',
            description='A thrilling adventure story.',
            author=self.author,
            editorial=self.editorial,
            detail=self.detail,
            sale=self.sale,
            created_by='test',
        )

        book.change_stock(10)
        assert book.stock == 10

        book.change_stock(-5)
        assert book.stock == 0
