from typing import Optional, cast

from src.domain.summary import TextGenerator, Summary


class TextGeneratorStub(TextGenerator):
    def __init__(self):
        self.text: str = 'Summary text'
        self._exception: Optional[Exception] = None

    def generate(self, summary: Summary) -> str:
        return self.text

    def error(self, exception: Exception | str) -> None:
        if isinstance(exception, str):
            exception = Exception(exception)
        self._exception = cast(Exception, exception)

    def _throw_error(self):
        if self._exception:
            raise self._exception
