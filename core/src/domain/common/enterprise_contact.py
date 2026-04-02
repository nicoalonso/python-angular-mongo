from dataclasses import dataclass


@dataclass
class EnterpriseContact:
    email: str = None
    website: str = None
    phone1: str = None
    phone2: str = None
