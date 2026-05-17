from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Abstract interface for embedding generation."""

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Number of dimensions in the output vector."""
        ...

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Returns embedding vector for a single text."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Returns embedding vectors for a batch of texts. More efficient than N embed_text calls."""
        ...
