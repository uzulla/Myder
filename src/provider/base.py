from abc import ABC, abstractmethod

class ProviderBase(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass