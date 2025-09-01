from abc import ABC, abstractmethod
from typing import Any, Dict


class OAuthSignIn(ABC):
    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    def authorize(self) -> Any: ...

    @abstractmethod
    def callback(self) -> Dict[str, Any]: ...

    def get_callback_url(self) -> str:
        # This should be implemented by subclasses if needed,
        # otherwise, it might be handled by the OAuth library directly.
        raise NotImplementedError
