from abc import ABC, abstractmethod
from typing import Any


class BaseModelProvider(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        response_schema: type[Any] | None = None,
    ) -> Any:
        pass