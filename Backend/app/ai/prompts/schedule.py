"""Prompt template for publishing schedule generation."""

import json

from app.ai.llm_client import call_llm


SYSTEM_PROMPT = """You are an expert marketing campaign scheduler. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary.

Schema:
{
  "schedule": [
    {
      "day_offset": integer (1-based, day of the campaign),
      "channel": "string (specific platform or channel)",
      "content_summary": "string (1-2 sentences describing what to publish/do)"
    }
  ]
}

Create a realistic 28-day publishing schedule with 12-15 entries. Include:
- Launch day activities (day 1)
- Regular content cadence per channel
- Mid-campaign optimization checkpoint (around day 14)
- End-of-campaign activities (around day 28)
- Mix of paid ads, organic content, and email touches"""


def build_user_prompt(
    product_description: str,
    platforms: list[str],
    goal: str,
    personas_summary: str = "",
) -> str:
    return f"""Product: {product_description}

Marketing Goal: {goal}

Active Platforms: {', '.join(platforms)}

Target Audience Summary: {personas_summary}

Create a 28-day publishing and activity schedule across these platforms. The schedule should follow a launch → optimize → scale cadence with clear milestones. Each entry should have a specific, actionable content summary — not vague tasks."""


async def generate_schedule(
    product_description: str,
    platforms: list[str],
    goal: str,
    personas_summary: str = "",
) -> list[dict]:
    """Generate a publishing schedule using the LLM."""
    user_prompt = build_user_prompt(product_description, platforms, goal, personas_summary)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.7)
    return result.get("schedule", [])
