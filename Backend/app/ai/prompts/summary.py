"""Prompt template for executive campaign summary generation."""

import json

from app.ai.llm_client import call_llm_for_text


SYSTEM_PROMPT = """You are a senior executive marketing strategist writing a comprehensive campaign summary. Write a 3-paragraph executive summary in natural prose.

Structure:
Paragraph 1: Strategic Overview & Audience Positioning — Synthesize the core product offering, target user personas, their primary pain points, and overall positioning strategy.
Paragraph 2: Multi-Channel Execution & Budget Strategy — Detail how the budget is allocated across channels (Google Search, Meta, LinkedIn, Content, etc.), why these channels suit this specific industry, and how ad messaging aligns with target audience intent.
Paragraph 3: Campaign Roadmap & Optimization Checkpoints — Outline the 28-day campaign execution roadmap, key milestones (launch, mid-campaign performance checkpoints, and scaling phase), and expected business outcomes.

IMPORTANT:
- DO NOT truncate product descriptions or use "..." snippets.
- DO NOT use generic template placeholders.
- Write a bespoke, executive-level narrative synthesizing all campaign inputs."""


def build_user_prompt(campaign_data: dict) -> str:
    return f"""Campaign Inputs and Data:
{json.dumps(campaign_data, indent=2, default=str)}

Write a bespoke, 3-paragraph executive summary synthesizing all sections of this campaign into a clear strategic narrative for decision-makers."""


async def generate_summary(campaign_data: dict) -> str:
    """Generate an executive summary from the full campaign data."""
    user_prompt = build_user_prompt(campaign_data)
    result = await call_llm_for_text(SYSTEM_PROMPT, user_prompt, temperature=0.7, max_tokens=1500)
    return result
