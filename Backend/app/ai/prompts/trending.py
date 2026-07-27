"""
AI Prompt builder and executor for real-time Trending Keywords generation using Tavily search.
"""
import logging
from typing import List, Dict, Any

from app.ai.llm_client import call_llm_with_tools
from app.ai.tools.tavily_tools import TAVILY_TOOLS_SCHEMA, TOOL_DISPATCH_MAP

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert digital marketing trends analyst.
Your task is to identify 4-6 real-time, highly relevant trending keywords and search topics for a marketing campaign.

Instructions:
1. You MUST use the `search_trending_keywords` tool to fetch real-time search trends and news for the given product and industry.
2. Based on the web search results, select high-growth, trending search phrases or industry topics.
3. Return a JSON object with a single key "trending_keywords" containing an array of objects:
{
  "trending_keywords": [
    {
      "keyword": "string (the trending keyword or phrase)",
      "reason": "string (why this keyword is trending and how to leverage it)"
    }
  ]
}
No Markdown formatting around the JSON object. Output ONLY valid JSON matching this schema.
"""

USER_PROMPT_TEMPLATE = """Product Description: {product}
Industry: {industry}

Use the `search_trending_keywords` tool to find current real-time trends for this product and industry, then return the trending keywords JSON array.
"""


async def generate_trending_keywords(product: str, industry: str) -> List[Dict[str, Any]]:
    """Generate grounded trending keywords using web search tools."""
    user_prompt = USER_PROMPT_TEMPLATE.format(product=product, industry=industry)
    try:
        result = await call_llm_with_tools(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            tools=TAVILY_TOOLS_SCHEMA,
            tool_dispatch_map=TOOL_DISPATCH_MAP,
            temperature=0.7,
        )

        if isinstance(result, dict) and "trending_keywords" in result:
            return result["trending_keywords"]
        elif isinstance(result, list):
            return result
        elif isinstance(result, dict) and "keywords" in result:
            return result["keywords"]

        logger.warning(f"Unexpected JSON schema from trending keywords LLM: {result}")
        return []
    except Exception as e:
        logger.error(f"Failed to generate trending keywords via LLM with tools: {e}")
        raise
