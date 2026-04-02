from dataclasses import dataclass


@dataclass
class BookDescriptor:
    id: str = None
    title: str = None
    isbn: str = None
