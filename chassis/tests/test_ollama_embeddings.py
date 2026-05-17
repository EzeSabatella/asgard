import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chassis.embeddings.ollama import OllamaEmbeddingProvider


@pytest.fixture
def mock_httpx():
    with patch("chassis.embeddings.ollama.httpx.AsyncClient") as mock_client_class:
        client_instance = MagicMock()
        mock_client_class.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        mock_client_class.return_value.__aexit__ = AsyncMock(return_value=False)

        # raise_for_status() y json() son síncronos en httpx — usar MagicMock
        text_response = MagicMock()
        text_response.json.return_value = {"embeddings": [[0.1] * 768]}

        batch_response = MagicMock()
        batch_response.json.return_value = {
            "embeddings": [[0.1] * 768, [0.2] * 768]
        }

        async def mock_post(url, json, timeout):
            if isinstance(json["input"], str):
                return text_response
            return batch_response

        client_instance.post = AsyncMock(side_effect=mock_post)
        yield client_instance


@pytest.mark.asyncio
async def test_embed_text_returns_correct_dimensions(mock_httpx):
    provider = OllamaEmbeddingProvider()
    result = await provider.embed_text("test")

    assert isinstance(result, list)
    assert len(result) == provider.dimensions
    assert result == [0.1] * 768


@pytest.mark.asyncio
async def test_embed_batch_returns_one_vector_per_text(mock_httpx):
    provider = OllamaEmbeddingProvider()
    texts = ["test 1", "test 2"]
    result = await provider.embed_batch(texts)

    assert isinstance(result, list)
    assert len(result) == len(texts)
    assert len(result[0]) == provider.dimensions


@pytest.mark.asyncio
async def test_embed_batch_single_call_to_api(mock_httpx):
    """embed_batch hace una sola llamada HTTP, no N llamadas."""
    provider = OllamaEmbeddingProvider()
    await provider.embed_batch(["a", "b", "c"])
    assert mock_httpx.post.call_count == 1
