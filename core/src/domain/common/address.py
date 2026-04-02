from dataclasses import dataclass


@dataclass
class Address:
    street: str = None
    postal_code: str = None
    city: str = None
    province: str = None
    country: str = None
