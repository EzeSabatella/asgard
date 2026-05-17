import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from chassis.llm.deepseek import DeepSeekLLMProvider


@pytest.fixture
def mock_openai():
    with patch("chassis.llm.deepseek.AsyncOpenAI") as mock_class:
        client_instance = mock_class.return_value

        completion = MagicMock()
        completion.choices = [MagicMock(message=MagicMock(content="respuesta de prueba"))]

        async def mock_create(**kwargs):
            return completion

        client_instance.chat.completions.create = AsyncMock(side_effect=mock_create)
        yield client_instance


@pytest.mark.asyncio
async def test_complete_returns_string(mock_openai):
    provider = DeepSeekLLMProvider(api_key="fake-key")
    messages = [
        {"role": "system", "content": "Sos un asistente."},
        {"role": "user", "content": "Hola"},
    ]
    result = await provider.complete(messages)

    assert isinstance(result, str)
    assert result == "respuesta de prueba"


@pytest.mark.asyncio
async def test_complete_uses_correct_model(mock_openai):
    provider = DeepSeekLLMProvider(api_key="fake-key", model="deepseek-chat")
    await provider.complete([{"role": "user", "content": "test"}])

    call_kwargs = mock_openai.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "deepseek-chat"


@pytest.mark.asyncio
async def test_complete_passes_messages(mock_openai):
    provider = DeepSeekLLMProvider(api_key="fake-key")
    messages = [{"role": "user", "content": "test"}]
    await provider.complete(messages)

    call_kwargs = mock_openai.chat.completions.create.call_args.kwargs
    assert call_kwargs["messages"] == messages
