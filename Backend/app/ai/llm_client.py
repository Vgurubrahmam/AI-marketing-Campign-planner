"""
Groq LLM client wrapper for real AI generation.
Calls Groq API with Llama 3.1 8B Instruct model.
Includes JSON parsing, retry on 429 rate limits, and fallback.
"""
import asyncio
import json
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    retry_on_fail: bool = True,
) -> dict | list | str:
    """
    Call the Groq API and parse the JSON response.
    Retries automatically on HTTP 429 (rate limits).
    """
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        max_attempts = 4
        for attempt in range(max_attempts):
            try:
                response = await client.post(
                    GROQ_API_URL, json=payload, headers=headers
                )

                if response.status_code == 429:
                    wait_sec = (attempt + 1) * 1.5
                    logger.warning(f"Groq API 429 rate limit hit. Waiting {wait_sec}s before retry...")
                    await asyncio.sleep(wait_sec)
                    continue

                response.raise_for_status()

                data = response.json()
                content = data["choices"][0]["message"]["content"]

                # Parse and return the JSON content
                parsed = json.loads(content)
                return parsed

            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error on attempt {attempt + 1}: {e}")
                if attempt == 0 and retry_on_fail:
                    payload["messages"][0]["content"] = (
                        "You MUST respond with valid JSON only. "
                        "No markdown, no code blocks, no commentary. "
                        "Just pure JSON matching the requested schema. "
                        + system_prompt
                    )
                    continue
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"Groq API HTTP error: {e.response.status_code}")
                if attempt < max_attempts - 1 and e.response.status_code == 429:
                    await asyncio.sleep((attempt + 1) * 2)
                    continue
                raise

            except Exception as e:
                logger.error(f"Groq API call failed: {e}")
                if attempt < max_attempts - 1:
                    await asyncio.sleep(1)
                    continue
                raise

        raise Exception("Exceeded max retries for Groq API call")


async def call_llm_for_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """Call the Groq API and return raw text (no JSON parsing)."""
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        for attempt in range(3):
            try:
                response = await client.post(GROQ_API_URL, json=payload, headers=headers)
                if response.status_code == 429:
                    await asyncio.sleep((attempt + 1) * 1.5)
                    continue
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt < 2:
                    await asyncio.sleep(1.5)
                    continue
                raise
