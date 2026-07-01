"""LLM provider service — wraps the Groq-compatible OpenAI client."""

from __future__ import annotations

import logging
from typing import Any

from openai import AsyncOpenAI

from app.core.settings import get_settings

logger = logging.getLogger(__name__)


class GroqLLMService:
    """Manages the Groq AsyncOpenAI client lifecycle and provides chat completion helpers."""

    def __init__(self) -> None:
        settings = get_settings()
        self.api_key: str = (settings.groq_api_key or "").strip()
        self.model: str = settings.groq_model
        self.base_url: str = settings.groq_base_url

        if self.api_key:
            self.client: AsyncOpenAI | None = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
            logger.info("GroqLLMService initialised (model=%s)", self.model)
        else:
            self.client = None
            logger.warning("No GROQ_API_KEY configured — LLM features disabled.")

    @property
    def is_available(self) -> bool:
        """True if the LLM client is configured and ready."""
        return self.client is not None and bool(self.api_key)

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.0,
    ) -> Any:
        """Call chat completions and return the raw API response."""
        if not self.is_available or self.client is None:
            raise RuntimeError("GroqLLMService is not configured. Set GROQ_API_KEY.")

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools

        return await self.client.chat.completions.create(**kwargs)
