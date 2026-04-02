from dataclasses import dataclass


@dataclass
class ContactInfo:
    email: str = None
    phone1: str = None
    phone2: str = None
