from typing import List
from openai import AsyncOpenAI
from chassis.llm.base import LLMProvider


class DeepSeekLLMProvider(LLMProvider):
    """
    DeepSeek LLM via OpenAI-compatible API.
    Default model: deepseek-chat (DeepSeek V3).
    """

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        temperature: float = 0.1,
    ):
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        self._model = model
        self._temperature = temperature

    async def complete(self, messages: List[dict]) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
        )
        return response.choices[0].message.content
