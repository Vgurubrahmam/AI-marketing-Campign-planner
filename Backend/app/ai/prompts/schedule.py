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

STRICT GENERATION RULES:
1. CURRENCY CONSISTENCY: All monetary figures (CPC, budget caps, CAC) MUST use ₹ (INR) or relative metrics. NEVER use dollar ($) signs or USD figures.
2. PERSONA NAMES: If referencing target audience personas by name in content summaries, use EXACT persona names provided in the user prompt (e.g. 'Simple Sarah', 'Mindful Mike'). NEVER combine, invent, or blend persona names (do NOT write 'Simple Mike').
3. Create a realistic 28-day publishing schedule with 8-12 entries following a Launch → Optimize → Scale cadence."""


def build_user_prompt(
    product_description: str,
    platforms: list[str],
    goal: str,
    personas_summary: str = "",
) -> str:
    return f"""Product: {product_description}

Marketing Goal: {goal}

Active Platforms: {', '.join(platforms)}

Target Audience Personas: {personas_summary}

Create a 28-day publishing and activity schedule across these platforms. The schedule should follow a launch → optimize → scale cadence with clear milestones. Each entry should have a specific, actionable content summary using INR (₹) for any currency metrics and exact persona names."""


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
