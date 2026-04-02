from .book_inspector import BookInspector

MIN_STOCK_FOR_SALE = 3


class BookSaleInspect(BookInspector):
    """
    Book inspector for checking if a book is available for sale.
    """
    async def available(self, book) -> bool:
        active_borrows = await self._obtain_active_borrows(book)
        available_stock = book.stock - active_borrows.count()
        return available_stock >= MIN_STOCK_FOR_SALE
