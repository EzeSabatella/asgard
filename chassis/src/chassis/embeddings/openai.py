from typing import List, Optional
from openai import AsyncOpenAI
from chassis.embeddings.base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """
    OpenAI embeddings via the official async client.
    Model default: text-embedding-3-small (1536 dimensions).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        dimensions: int = 1536,
    ):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model
        self._dimensions = dimensions

    @property
    def dimensions(self) -> int:
        return self._dimensions

    async def embed_text(self, text: str) -> List[float]:
        response = await self._client.embeddings.create(
            input=text,
            model=self._model,
        )
        return response.data[0].embedding

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = await self._client.embeddings.create(
            input=texts,
            model=self._model,
        )
        return [item.embedding for item in response.data]
