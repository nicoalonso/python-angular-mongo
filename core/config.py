from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""

    # Database settings
    database_url: str = Field(description="The URL of the MongoDB database.", default="")
    database_name: str = Field(description="The name of the MongoDB database.", default="")
    # RabbitMQ settings
    rabbitmq_dsn: str = Field(description="The DSN for connecting to RabbitMQ.", default="")
    rabbitmq_exchange: str = Field(description="The name of the RabbitMQ exchange.", default="")
    rabbitmq_queue: str = Field(description="The name of the RabbitMQ queue.", default="")
    # OpenAI settings
    openai_api_key: SecretStr = Field(description="The API key for OpenAI.", default="")
    openai_model: str = Field(description="The model to use for OpenAI.", default="")

    # API settings
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


@lru_cache
def get_settings():
    return Settings()
