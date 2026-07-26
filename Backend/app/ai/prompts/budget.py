"""Prompt template for budget reasoning (numbers are deterministic, LLM provides reasoning only)."""

import json

from app.ai.llm_client import call_llm


SYSTEM_PROMPT = """You are an expert marketing budget strategist. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary.

Schema:
{
  "reasoning": [
    {
      "channel": "string (must match one of the provided channels exactly)",
      "reasoning": "string (2-3 sentences explaining why this allocation makes sense)"
    }
  ]
}

STRICT CONSTRAINTS:
1. B2C vs B2B RULE: Check if the business/product is B2C (e.g. consumer products, home cleaning, retail, skincare). For B2C campaigns, NEVER label LinkedIn or any channel as 'B2B'. Instead, describe LinkedIn as reaching affluent professionals or career-minded consumers in their personal capacity.
2. Provide strategic reasoning for each budget allocation. Reference the specific marketing goal, industry context, and target personas when explaining allocations."""


def build_user_prompt(
    goal: str,
    industry: str,
    budget_amount: float,
    allocations: list[dict],
    personas_summary: str = "",
) -> str:
    return f"""Marketing Goal: {goal}
Industry: {industry}
Total Budget: ₹{budget_amount:,.2f}

Budget Allocations (already determined):
{json.dumps(allocations, indent=2)}

Target Audience Summary: {personas_summary}

For each channel allocation above, provide strategic reasoning explaining why this percentage makes sense for this specific goal, industry, and audience. Be specific — reference the goal and personas, not generic advice."""


async def generate_budget_reasoning(
    goal: str,
    industry: str,
    budget_amount: float,
    allocations: list[dict],
    personas_summary: str = "",
) -> list[dict]:
    """Generate reasoning text for pre-computed budget allocations."""
    user_prompt = build_user_prompt(goal, industry, budget_amount, allocations, personas_summary)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.6)
    return result.get("reasoning", [])
