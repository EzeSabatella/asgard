import os
from chassis.embeddings.base import EmbeddingProvider
from chassis.embeddings.openai import OpenAIEmbeddingProvider
from chassis.embeddings.ollama import OllamaEmbeddingProvider


def create_embedding_provider(config) -> EmbeddingProvider:
    if config.provider == "ollama":
        return OllamaEmbeddingProvider(
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=config.model,
            dimensions=config.dimensions,
        )
    if config.provider == "openai":
        return OpenAIEmbeddingProvider(
            api_key=os.environ["OPENAI_API_KEY"],
            model=config.model,
            dimensions=config.dimensions,
        )
    raise ValueError(f"Unknown embedding provider: {config.provider}")


__all__ = [
    "EmbeddingProvider",
    "OpenAIEmbeddingProvider",
    "OllamaEmbeddingProvider",
    "create_embedding_provider",
]
