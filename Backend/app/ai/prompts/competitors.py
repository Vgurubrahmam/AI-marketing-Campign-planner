"""
AI Prompt builder and executor for real-time Competitor Research generation using Tavily search.
"""
import logging
from typing import List, Dict, Any

from app.ai.llm_client import call_llm_with_tools
from app.ai.tools.tavily_tools import TAVILY_TOOLS_SCHEMA, TOOL_DISPATCH_MAP

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a strategic competitive intelligence analyst.
Your task is to identify 3-5 real market competitors and analyze their positioning and differentiator opportunities for a marketing campaign.

Instructions:
1. You MUST use the `search_competitors` tool to research actual competitors and market alternatives for the product/industry.
2. For each competitor, evaluate their current market positioning and identify a key opportunity where our product can differentiate.
3. Return a JSON object with a single key "competitors" containing an array of objects:
{
  "competitors": [
    {
      "name": "string (Competitor Brand Name)",
      "positioning": "string (How they position themselves in the market)",
      "differentiator_opportunity": "string (How our campaign/product can outperform or differentiate against them)"
    }
  ]
}
No Markdown formatting around the JSON object. Output ONLY valid JSON matching this schema.
"""

USER_PROMPT_TEMPLATE = """Product Description: {product}
Industry: {industry}

Use the `search_competitors` tool to discover competitors, analyze their positioning, and return the competitor research JSON.
"""


async def generate_competitors(product: str, industry: str) -> List[Dict[str, Any]]:
    """Generate grounded competitor research using web search tools."""
    user_prompt = USER_PROMPT_TEMPLATE.format(product=product, industry=industry)
    try:
        result = await call_llm_with_tools(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            tools=TAVILY_TOOLS_SCHEMA,
            tool_dispatch_map=TOOL_DISPATCH_MAP,
            temperature=0.7,
        )

        if isinstance(result, dict) and "competitors" in result:
            return result["competitors"]
        elif isinstance(result, list):
            return result

        logger.warning(f"Unexpected JSON schema from competitor research LLM: {result}")
        return []
    except Exception as e:
        logger.error(f"Failed to generate competitor research via LLM with tools: {e}")
        raise
