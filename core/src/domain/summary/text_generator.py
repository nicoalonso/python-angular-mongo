from abc import ABC

from src.domain.summary import Summary


class TextGenerator(ABC):
    """
    Interface for text generation
    """
    def generate(self, summary: Summary) -> str: ...
