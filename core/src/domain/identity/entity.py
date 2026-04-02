from datetime import datetime
from dataclasses import dataclass, field

from .identity import Identity


@dataclass
class Entity(Identity):
  """
    Base class for all entities in the domain.
    It provides common properties and methods for tracking creation and update information.

    Attributes:
        created_by (str): The identifier of the user who created the entity.
        created_at (datetime): The timestamp when the entity was created.
        updated_by (str | None): The identifier of the user who last updated the entity.
        updated_at (datetime | None): The timestamp when the entity was last updated.
  """
  created_by: str = ''
  created_at: datetime = field(default_factory=lambda: datetime.now())
  updated_by: str | None = None
  updated_at: datetime | None = None

  def updated(self, updated_by: str) -> None:
    """
    Method to update the entity's update information.
    :param updated_by: (string) The identifier of the user who is updating the entity information.
    """
    self.updated_by = updated_by
    self.updated_at = datetime.now()
