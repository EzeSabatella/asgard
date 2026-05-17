import pytest
from unittest.mock import MagicMock, patch
from chassis.embeddings.openai import OpenAIEmbeddingProvider

@pytest.fixture
def mock_openai():
    with patch("chassis.embeddings.openai.AsyncOpenAI") as mock:
        client_instance = mock.return_value
        
        # Mock create() response for embed_text
        text_response = MagicMock()
        text_response.data = [MagicMock(embedding=[0.1] * 1536)]
        
        # Mock create() response for embed_batch
        batch_response = MagicMock()
        batch_response.data = [
            MagicMock(embedding=[0.1] * 1536),
            MagicMock(embedding=[0.2] * 1536)
        ]
        
        # We need the mock to return different things depending on input or just a generic mock
        async def mock_create(input, model):
            if isinstance(input, str):
                return text_response
            return batch_response
            
        client_instance.embeddings.create = MagicMock(side_effect=mock_create)
        yield client_instance

@pytest.mark.asyncio
async def test_embed_text_returns_correct_dimensions(mock_openai):
    """embed_text retorna lista de floats con longitud == provider.dimensions."""
    provider = OpenAIEmbeddingProvider(api_key="fake-key")
    result = await provider.embed_text("test")
    
    assert isinstance(result, list)
    assert len(result) == provider.dimensions
    assert result == [0.1] * 1536
    mock_openai.embeddings.create.assert_called_once()

@pytest.mark.asyncio
async def test_embed_batch_returns_one_vector_per_text(mock_openai):
    """embed_batch retorna una lista con la misma longitud que la entrada."""
    provider = OpenAIEmbeddingProvider(api_key="fake-key")
    texts = ["test 1", "test 2"]
    result = await provider.embed_batch(texts)
    
    assert isinstance(result, list)
    assert len(result) == len(texts)
    assert len(result[0]) == provider.dimensions
    mock_openai.embeddings.create.assert_called_once()
