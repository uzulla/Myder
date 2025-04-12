from .base import ProviderBase

class OpenRouterProvider(ProviderBase):
    @property
    def name(self) -> str:
        return "openrouter"

    @property
    def base_url(self) -> str:
        return "https://openrouter.ai/api/v1"

    def run(self, model=None):
        return f"Provider: {self.name}, Base URL: {self.base_url}, API Key: {self.api_key}, Model: {model}"