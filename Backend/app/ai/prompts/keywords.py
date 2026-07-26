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

CRITICAL RULES:
1. GROUND IN THE SPECIFIC PRODUCT: Extract keywords that directly describe the exact product type (e.g., skincare, facial cleanser, freelance accounting, organic snacks).
2. DO NOT use generic software/SaaS suffixes ("app", "software", "tool", "platform") unless the product is explicitly a software application!
3. DO NOT treat business model descriptors like "direct-to-consumer" or "d2c" as the main product noun. Extract the actual product/service being sold (e.g. "minimalist skincare routine", "sensitive skin moisturizer").
4. Provide 10-15 keywords with a healthy mix of transactional (buy/order/pricing), informational (how to/benefits/guide), and long-tail terms."""


def build_user_prompt(product_description: str, industry: str, ad_copy_context: str = "") -> str:
    return f"""Product/Service Description: {product_description}

Industry: {industry}

{f'Ad Copy Context (for keyword grounding): {ad_copy_context}' if ad_copy_context else ''}

Generate 10-15 hyper-relevant search keywords that customers search for when looking for this specific product or solving the exact problem it addresses."""


async def generate_keywords(product_description: str, industry: str, ad_copy_context: str = "") -> list[dict]:
    """Generate keywords with intent classification using the LLM."""
    user_prompt = build_user_prompt(product_description, industry, ad_copy_context)
    result = await call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.5)
    return result.get("keywords", [])
