"""
Mock AI client that returns dynamic stub responses based on the actual input product description,
industry, and marketing goal. Used when USE_MOCK_AI=true.
"""
import asyncio
import random


def _extract_product_title(product_description: str) -> str:
    """Extract a brief product subject line from the description."""
    first_sentence = product_description.strip().split('.')[0]
    if len(first_sentence) > 60:
        return first_sentence[:60] + "..."
    return first_sentence


async def generate_mock_personas(product_description: str, industry: str, goal: str) -> list[dict]:
    """Return dynamic mock audience personas tailored to the input product."""
    await asyncio.sleep(random.uniform(0.5, 1.2))
    prod_title = _extract_product_title(product_description)
    ind = industry.replace('_', ' ').capitalize()

    return [
        {
            "persona_name": f"Target {ind} User",
            "demographics": {
                "age_range": "25-45",
                "gender": "Mixed",
                "income": "Mid to High Income",
                "education": "Bachelor's Degree",
                "location": "Metro & Urban areas",
            },
            "pain_points": [
                f"Needs efficient solutions for {prod_title.lower()}",
                "Time-consuming manual workflows and disorganization",
                "High operational overhead and tracking errors",
                "Seeking easy-to-adopt software with proven reliability",
            ],
            "channels": ["Google Search", "LinkedIn", "Industry Communities", "Email"],
            "messaging_angle": f"Focus on core value proposition: simplify {prod_title.lower()} with intuitive, hassle-free management.",
        },
        {
            "persona_name": f"Budget-Conscious {ind} Operator",
            "demographics": {
                "age_range": "28-50",
                "gender": "Mixed",
                "income": "Moderate Income",
                "education": "College / Self-taught",
                "location": "Suburban & Regional",
            },
            "pain_points": [
                "Strict budget limitations and price sensitivity",
                "Overwhelmed by overly complex enterprise tools",
                "Needs fast setup with immediate ROI",
            ],
            "channels": ["Facebook", "Instagram", "Google Search", "YouTube Tutorials"],
            "messaging_angle": f"Highlight affordability and quick setup for {prod_title.lower()} without hidden costs.",
        },
        {
            "persona_name": "Growth & Scale Advocate",
            "demographics": {
                "age_range": "30-48",
                "gender": "Mixed",
                "income": "High Income",
                "education": "Graduate Degree",
                "location": "Major Tech & Commercial Hubs",
            },
            "pain_points": [
                "Scaling bottleneck with legacy manual tools",
                "Lack of real-time visibility and analytics",
                "Team alignment and reporting overhead",
            ],
            "channels": ["LinkedIn", "Twitter/X", "Tech Newsletters", "Podcasts"],
            "messaging_angle": f"Emphasize scalability, automated insights, and performance optimization.",
        },
    ]


async def generate_mock_ad_copy(
    product_description: str, persona: dict, platform: str
) -> dict:
    """Return dynamic mock ad copy tailored to product description and platform."""
    await asyncio.sleep(random.uniform(0.3, 0.7))
    prod_title = _extract_product_title(product_description)

    copies = {
        "google": {
            "headline": f"Simplify {prod_title[:30]} Today",
            "body": f"Designed for users who want better control and performance. Save time, reduce friction, and achieve your goal faster. Get started free.",
            "cta": "Try It Free",
        },
        "meta": {
            "headline": f"The Smarter Way to Manage {prod_title[:25]}",
            "body": f"Stop struggling with complex manual processes. Experience seamless tracking, automated insights, and effortless control.",
            "cta": "Learn More",
        },
        "linkedin": {
            "headline": f"Streamline Your Workflows with {prod_title[:25]}",
            "body": f"Top professionals choose intelligent automation to boost productivity and reduce cost. See how easy setup can transform your results.",
            "cta": "Request Demo",
        },
        "instagram": {
            "headline": f"Better Results, Less Effort ✨",
            "body": f"Take total control of {prod_title[:30].lower()} with our easy-to-use platform. Built for modern creators and professionals.",
            "cta": "Get Started",
        },
    }

    return copies.get(platform, copies["google"])


async def generate_mock_keywords(product_description: str) -> list[dict]:
    """Return dynamic mock keywords tailored to the product description."""
    await asyncio.sleep(random.uniform(0.4, 0.8))
    words = [w.strip(',.').lower() for w in product_description.split() if len(w) > 4][:5]
    base_terms = words if words else ["solution", "software", "tool", "app"]

    return [
        {"keyword": f"{base_terms[0]} app", "keyword_type": "seo", "intent": "transactional", "relevance_score": 0.95},
        {"keyword": f"best {base_terms[0]} tool", "keyword_type": "seo", "intent": "transactional", "relevance_score": 0.92},
        {"keyword": f"how to manage {base_terms[0]}", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.88},
        {"keyword": f"automated {base_terms[-1]} software", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.85},
        {"keyword": f"top {base_terms[0]} software 2025", "keyword_type": "ppc", "intent": "transactional", "relevance_score": 0.90},
        {"keyword": f"affordable {base_terms[0]} for business", "keyword_type": "ppc", "intent": "transactional", "relevance_score": 0.87},
        {"keyword": f"{base_terms[-1]} optimization tips", "keyword_type": "ppc", "intent": "informational", "relevance_score": 0.84},
        {"keyword": f"cloud {base_terms[0]} platform", "keyword_type": "seo", "intent": "navigational", "relevance_score": 0.82},
    ]


async def generate_mock_budget(
    goal: str, industry: str, budget_amount: float
) -> list[dict]:
    """Return dynamic budget allocation based on total budget amount."""
    await asyncio.sleep(random.uniform(0.3, 0.6))
    allocations = [
        {"channel": "Google Search Ads", "allocation_percent": 35.0, "reasoning": "High-intent search captures prospects actively seeking solutions with clear ROI."},
        {"channel": "Social Media Ads (Meta/LinkedIn)", "allocation_percent": 30.0, "reasoning": "Targeted audience reach and visual engagement for brand awareness and retargeting."},
        {"channel": "Content Marketing & SEO", "allocation_percent": 15.0, "reasoning": "Long-term organic acquisition engine building authority and organic domain rank."},
        {"channel": "Email Nurture & Retention", "allocation_percent": 12.0, "reasoning": "Low cost per lead nurturing channel with high conversion efficiency for trial users."},
        {"channel": "Influencers & Strategic Partners", "allocation_percent": 8.0, "reasoning": "Targeted partner co-marketing to gain trust in niche industry circles."},
    ]

    for alloc in allocations:
        alloc["amount"] = round(budget_amount * alloc["allocation_percent"] / 100, 2)

    return allocations


async def generate_mock_schedule(ad_copies: list, duration_weeks: int = 4) -> list[dict]:
    """Return dynamic publishing schedule."""
    await asyncio.sleep(random.uniform(0.3, 0.6))
    return [
        {"day_offset": 1, "channel": "Google Search", "content_summary": "Launch targeted high-intent search ads with primary feature keywords."},
        {"day_offset": 2, "channel": "LinkedIn / Meta", "content_summary": "Publish core problem-agitation-solution awareness campaign."},
        {"day_offset": 5, "channel": "Blog & Content", "content_summary": "Publish comprehensive guide addressing top customer pain points."},
        {"day_offset": 8, "channel": "Email Campaign", "content_summary": "Send announcement email sequence to early subscriber segment."},
        {"day_offset": 14, "channel": "Performance Review", "content_summary": "Analyze early CTR and CPC metrics; shift budget to top performing ad variants."},
        {"day_offset": 21, "channel": "Retargeting Ads", "content_summary": "Deploy retargeting ads to engaged visitors with social proof / testimonials."},
        {"day_offset": 28, "channel": "Monthly Scaling", "content_summary": "Review final cost per acquisition (CAC) and scale winning campaign assets."},
    ]


async def generate_mock_summary(campaign_data: dict) -> str:
    """Return dynamic campaign summary based on actual input campaign data."""
    await asyncio.sleep(random.uniform(0.3, 0.6))
    product = campaign_data.get("product_description", "the product")
    prod_title = _extract_product_title(product)
    goal = campaign_data.get("marketing_goal", "growth").replace("_", " ")
    industry = campaign_data.get("industry", "general").capitalize()
    budget = campaign_data.get("budget_amount", 0)

    return (
        f"This strategic marketing campaign is tailored for '{prod_title}' within the {industry} industry, "
        f"focused on achieving the primary goal of {goal}. With an allocated budget of ₹{budget:,.2f}, "
        f"the campaign deploys a high-impact multi-channel strategy spanning Google Search, Meta, LinkedIn, and Content Marketing. "
        f"The plan targets key user personas facing core operational pain points, combining high-intent search acquisition "
        f"with visual social ads and long-term content authority. The 28-day schedule follows a structured "
        f"launch-optimize-scale roadmap with performance optimization checkpoints at Day 14 and Day 28."
    )
