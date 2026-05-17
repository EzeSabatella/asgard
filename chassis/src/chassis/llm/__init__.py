import os
from chassis.llm.base import LLMProvider
from chassis.llm.deepseek import DeepSeekLLMProvider


def create_llm_provider(config) -> LLMProvider:
    if config.provider == "deepseek":
        return DeepSeekLLMProvider(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            model=config.model,
            temperature=config.temperature,
        )
    raise ValueError(f"Unknown LLM provider: {config.provider}")


__all__ = ["LLMProvider", "DeepSeekLLMProvider", "create_llm_provider"]
