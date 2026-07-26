"""Prompt template for platform-specific ad copy generation across all platforms in a single LLM call."""

import json

from app.ai.llm_client import call_llm

PLATFORMS = ["google", "meta", "linkedin", "instagram"]

PLATFORM_LIMITS = {
    "google": {"headline_max": 30, "body_max": 90, "description": "Google Ads search ad"},
    "meta": {"headline_max": 40, "body_max": 125, "description": "Facebook/Instagram feed ad"},
    "linkedin": {"headline_max": 70, "body_max": 150, "description": "LinkedIn sponsored content"},
    "instagram": {"headline_max": 40, "body_max": 125, "description": "Instagram story/feed ad"},
}

SYSTEM_PROMPT = """You are an expert digital advertising copywriter. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary.

Schema:
{
  "ad_copies": [
    {
      "platform": "string (one of: google, meta, linkedin, instagram)",
      "headline": "string (compelling, within character limit for platform)",
      "body": "string (persuasive copy within character limit for platform)",
      "cta": "string (clear call-to-action, 2-5 words)"
    }
  ]
}

Write high-converting ad copy for all 4 specified platforms (google, meta, linkedin, instagram). Ensure character limits per platform are respected."""


def build_user_prompt(
    product_description: str, persona: dict
) -> str:
    return f"""Product: {product_description}

Target Persona: {json.dumps(persona, indent=2)}

Platform Character Limits:
- google: Headline max 30 chars, Body max 90 chars
- meta: Headline max 40 chars, Body max 125 chars
- linkedin: Headline max 70 chars, Body max 150 chars
- instagram: Headline max 40 chars, Body max 125 chars

Write high-converting ad copy for each of the 4 platforms (google, meta, linkedin, instagram). The copy should speak directly to the persona's pain points."""


async def generate_all_ad_copies(
    product_description: str, persona: dict
) -> list[dict]:
    """Generate ad copy for all 4 platforms in a single fast LLM call."""
    user_prompt = build_user_prompt(product_description, persona)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.8)
    return result.get("ad_copies", [])


async def generate_ad_copy(
    product_description: str, persona: dict, platform: str
) -> dict:
    """Fallback single platform ad copy generator."""
    copies = await generate_all_ad_copies(product_description, persona)
    for c in copies:
        if c.get("platform") == platform:
            return c
    return {
        "platform": platform,
        "headline": f"Discover {product_description[:25]}",
        "body": "Streamline your workflows and boost productivity starting today.",
        "cta": "Learn More",
    }
