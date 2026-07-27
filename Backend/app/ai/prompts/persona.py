"""Prompt template for audience persona generation."""

from app.ai.llm_client import call_llm


SYSTEM_PROMPT = """You are an expert marketing strategist. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary, no code blocks.

Schema:
{
  "personas": [
    {
      "persona_name": "string (creative, descriptive name)",
      "demographics": {
        "age_range": "string",
        "gender": "string",
        "income": "string (e.g. ₹5,00,000 - ₹8,00,000 / year or ₹50,000 - ₹80,000 / month)",
        "education": "string",
        "location": "string"
      },
      "pain_points": ["string (4-5 specific pain points)"],
      "channels": ["string (3-4 preferred marketing channels - use Title Case like 'Google Ads (Search)', 'Meta Ads (Instagram)', 'Content Marketing & SEO', 'Email Marketing')"],
      "messaging_angle": "string (2-3 sentences on how to position the product for this persona)"
    }
  ]
}

STRICT CURRENCY RULE:
All income figures MUST use ₹ (INR) (e.g. ₹5,00,000 - ₹8,00,000 / year or ₹50,000 - ₹80,000 / month). NEVER use dollar ($) signs under any circumstances.

Generate exactly 3 distinct audience personas. Make them specific and actionable, not generic."""


def build_user_prompt(product_description: str, industry: str, goal: str) -> str:
    return f"""Product/Service Description: {product_description}

Industry: {industry}

Marketing Goal: {goal}

Based on this product and its market context, generate 3 distinct audience personas that would be most responsive to this product. Each persona should represent a meaningfully different segment with unique pain points and channel preferences using INR (₹) for all income figures."""


async def generate_personas(product_description: str, industry: str, goal: str) -> list[dict]:
    """Generate audience personas using the LLM."""
    user_prompt = build_user_prompt(product_description, industry, goal)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.7)
    return result.get("personas", [])
