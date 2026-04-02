from dataclasses import dataclass


@dataclass
class CustomerDescriptor:
    id: str = None
    name: str = None
    surname: str = None
    vat_number: str = None
    number: str = None
