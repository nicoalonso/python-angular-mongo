from src.domain.identity.exception import NotFoundError


class ProviderNotFoundError(NotFoundError):
    def __init__(self, provider_id: str):
        self.provider_id = provider_id
        super().__init__(f"Provider with ID {provider_id} not found.")
