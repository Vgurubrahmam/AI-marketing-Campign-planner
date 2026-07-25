"""Prompt template for executive campaign summary generation."""

import json

from app.ai.llm_client import call_llm_for_text


SYSTEM_PROMPT = """You are a senior marketing strategist writing an executive summary. Write a clear, concise 3-5 paragraph summary. No JSON — write natural prose.

Cover:
1. Campaign overview (target audience, channels, positioning)
2. Key strategic decisions and rationale
3. Budget allocation highlights
4. Expected outcomes and timeline
5. Recommended next steps

Keep it professional but readable — this is for stakeholders who need to quickly understand the campaign strategy."""


def build_user_prompt(campaign_data: dict) -> str:
    return f"""Campaign Data:
{json.dumps(campaign_data, indent=2, default=str)}

Write an executive summary synthesizing all sections of this campaign into a coherent strategic narrative. Reference specific personas, channels, budget amounts, and timeline milestones."""


async def generate_summary(campaign_data: dict) -> str:
    """Generate an executive summary from the full campaign data."""
    user_prompt = build_user_prompt(campaign_data)
    result = await call_llm_for_text(SYSTEM_PROMPT, user_prompt, temperature=0.6)
    return result
