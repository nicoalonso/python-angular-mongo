from dataclasses import dataclass

ADMIN_GROUP = 'admin'


@dataclass
class User:
    name: str
    display_name: str
    groups: list[str]

    def is_admin(self) -> bool:
        return ADMIN_GROUP in self.groups
