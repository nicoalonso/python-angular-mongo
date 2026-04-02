from dataclasses import dataclass


@dataclass
class BookSale:
    saleable: bool = None
    price: float = None
    discount: float = None
