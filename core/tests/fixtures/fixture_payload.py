import json
from pathlib import Path
from typing import Any


class FixturePayload:
    """
    Load a fixture payload from a file and return it as a dictionary.
    The payload can be overrides by passing a dictionary.
    """
    def __init__(self):
        self._overrides: dict[str, Any] = {}

    def override(self, **overrides) -> "FixturePayload":
        """Set overrides for the fixture payload. Supports method chaining."""
        self._overrides = overrides
        return self

    def load(self, name: str, **overrides) -> dict[str, Any]:
        """
        Load a fixture from a JSON file and merge with overrides.

        Args:
            name: Name of the fixture file (without .json extension)

        Returns:
            Merged dictionary with fixture data and overrides

        Raises:
            FileNotFoundError: If the fixture file doesn't exist
        """
        file_path = Path(__file__).parent / "payload" / f"{name}.json"

        if not file_path.exists():
            raise FileNotFoundError(f"Fixture not found: {file_path}")

        raw = file_path.read_text(encoding='utf-8')
        data: dict[str, Any] = json.loads(raw)

        return {**data, **self._overrides, **overrides}
