from pathlib import Path
from string import Template
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.domain.summary import Summary, TextGenerator, SummaryType
from .summary_response import SummaryResponse


class OpenAITextGenerator(TextGenerator):
    """
    OpenAI Text Generator
    """
    def __init__(self, model: str, api_key: SecretStr):
        self._model = model
        self._api_key = api_key

    def generate(self, summary: Summary) -> str:
        """
        Generates text based on the input URL.
        :param summary: Summary object containing the URL and other information
        :return: Generated text
        """
        template = self._load_prompt(summary.type)
        prompt = template.safe_substitute(url=summary.url)

        return self._generate(prompt)

    def _generate(self, prompt: str) -> str:
        """
        Generates text using the provided prompt.
        :param prompt: Prompt string to generate text from
        :return: Generated text
        """
        llm = ChatOpenAI(
            model=self._model,
            api_key=self._api_key,
            temperature=0,
        )

        structured_llm = llm.with_structured_output(SummaryResponse)

        messages = [
            SystemMessage(content="Responde solo con los campos solicitados"),
            HumanMessage(content=prompt),
        ]

        text = ''
        response = cast(SummaryResponse, structured_llm.invoke(messages))
        if response and response.summary:
            text = response.summary

        return text.strip("'\n ")

    @staticmethod
    def _load_prompt(type_: SummaryType) -> Template:
        """
        Loads the appropriate prompt based on the summary type.
        :param type_: Type of summary (e.g., TITLE, DESCRIPTION)
        :return: Prompt string
        """
        file_path = Path(__file__).parent / "prompts"
        match type_:
            case SummaryType.DESCRIPTION:
                filename = "book_summary"
            case SummaryType.BIOGRAPHY:
                filename = "author_biography"
            case _:
                raise ValueError("Unsupported summary type: " + str(type_))

        file_path = file_path / f"{filename}.txt"
        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        raw = file_path.read_text(encoding='utf-8')
        return Template(raw)
