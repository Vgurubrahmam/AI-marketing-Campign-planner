"""Prompt template for platform-specific ad copy generation."""

import json

from app.ai.llm_client import call_llm

PLATFORM_LIMITS = {
    "google": {"headline_max": 30, "body_max": 90, "description": "Google Ads search ad"},
    "meta": {"headline_max": 40, "body_max": 125, "description": "Facebook/Instagram feed ad"},
    "linkedin": {"headline_max": 70, "body_max": 150, "description": "LinkedIn sponsored content"},
    "instagram": {"headline_max": 40, "body_max": 125, "description": "Instagram story/feed ad"},
}

SYSTEM_PROMPT = """You are an expert digital advertising copywriter. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary.

Schema:
{
  "headline": "string (compelling, within character limit)",
  "body": "string (persuasive copy within character limit)",
  "cta": "string (clear call-to-action, 2-5 words)"
}

Write copy that is specific, benefit-driven, and emotionally engaging. Avoid generic marketing fluff."""


def build_user_prompt(
    product_description: str, persona: dict, platform: str
) -> str:
    limits = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS["google"])
    return f"""Product: {product_description}

Target Persona: {json.dumps(persona, indent=2)}

Platform: {limits['description']}
Character limits: Headline max {limits['headline_max']} chars, Body max {limits['body_max']} chars

Write a single, high-converting ad for this specific persona on this specific platform. The copy should speak directly to their pain points and use language appropriate for the platform."""


async def generate_ad_copy(
    product_description: str, persona: dict, platform: str
) -> dict:
    """Generate platform-specific ad copy using the LLM."""
    user_prompt = build_user_prompt(product_description, persona, platform)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.8)
    return result
