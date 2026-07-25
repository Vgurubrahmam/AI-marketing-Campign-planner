"""Prompt template for keyword extraction with intent classification."""

from app.ai.llm_client import call_llm


SYSTEM_PROMPT = """You are an expert SEO/PPC strategist. Respond ONLY with valid JSON matching the exact schema below. No markdown, no commentary.

Schema:
{
  "keywords": [
    {
      "keyword": "string (2-5 word phrase)",
      "keyword_type": "seo" | "ppc",
      "intent": "informational" | "transactional" | "navigational",
      "relevance_score": 0.0-1.0
    }
  ]
}

Generate 10-15 keywords. Include a mix of:
- High-intent transactional keywords (people ready to buy/sign up)
- Informational keywords (people researching the problem space)
- Long-tail variations that are specific to the product
- Both SEO (organic content targets) and PPC (paid ad targets)

Rank by relevance_score where 1.0 = perfectly relevant to the product."""


def build_user_prompt(product_description: str, industry: str, ad_copy_context: str = "") -> str:
    return f"""Product/Service Description: {product_description}

Industry: {industry}

{f'Ad Copy Context (for keyword grounding): {ad_copy_context}' if ad_copy_context else ''}

Extract and generate keywords that a potential customer would search for when looking for this product or solutions to the problems it solves. Ground keywords in the actual product description — avoid generic industry terms unless they're genuinely relevant."""


async def generate_keywords(product_description: str, industry: str, ad_copy_context: str = "") -> list[dict]:
    """Generate keywords with intent classification using the LLM."""
    user_prompt = build_user_prompt(product_description, industry, ad_copy_context)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.5)
    return result.get("keywords", [])
