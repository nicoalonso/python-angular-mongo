from .book_inspector import BookInspector


class BookBorrowInspect(BookInspector):
    """
    Book inspector for checking if a book is available for borrowing.
    """
    async def available(self, book) -> bool:
        active_borrows = await self._obtain_active_borrows(book)
        return book.stock > active_borrows.count()
