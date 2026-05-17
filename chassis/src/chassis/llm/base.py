from abc import ABC, abstractmethod
from typing import List


class LLMProvider(ABC):
    """Abstract interface for LLM text completion."""

    @abstractmethod
    async def complete(self, messages: List[dict]) -> str:
        """
        OpenAI-format messages: [{"role": "system|user|assistant", "content": "..."}]
        Returns the assistant's response text.
        """
        ...
