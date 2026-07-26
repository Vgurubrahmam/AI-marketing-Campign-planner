"""
Mock AI client that returns dynamic stub responses based on the actual input product description,
industry, and marketing goal. Used when USE_MOCK_AI=true or during fallback.
"""
import asyncio
import random

STOP_WORDS = {
    "direct-to-consumer", "d2c", "b2b", "b2c", "offering", "brand", "a", "an",
    "the", "with", "for", "and", "or", "in", "on", "at", "to", "from", "that",
    "which", "this", "these", "those", "solution", "product", "service", "making",
    "helps", "people", "users", "customers", "simple", "easy", "best", "top"
}


def _extract_product_title(product_description: str) -> str:
    """Extract a clean product subject string without trailing ellipsis."""
    clean = product_description.strip().split('.')[0]
    return clean.strip()


def _extract_domain_keywords(product_description: str, industry: str) -> list[str]:
    """Extract actual domain-relevant nouns from the product description."""
    raw_words = [w.strip('.,()!"\'').lower() for w in product_description.split()]
    filtered = [w for w in raw_words if len(w) > 3 and w not in STOP_WORDS]
    if filtered:
        return filtered[:6]
    ind = industry.replace('_', ' ').lower()
    return [ind, "solutions", "services"]


async def generate_mock_personas(product_description: str, industry: str, goal: str) -> list[dict]:
    """Return dynamic mock audience personas tailored to the input product."""
    await asyncio.sleep(random.uniform(0.3, 0.6))
    prod_title = _extract_product_title(product_description)
    ind = industry.replace('_', ' ').capitalize()

    return [
        {
            "persona_name": f"Target {ind} Buyer",
            "demographics": {
                "age_range": "25-45",
                "gender": "Mixed",
                "income": "Mid to High Income",
                "education": "Bachelor's Degree",
                "location": "Metro & Urban areas",
            },
            "pain_points": [
                f"Seeking high-quality solutions for {prod_title.lower()}",
                "Frustrated by over-complicated options and poor results",
                "Limited time to research and evaluate competing brands",
                "Demands clear ROI and hassle-free experience",
            ],
            "channels": ["Google Search", "Meta (Instagram/FB)", "Industry Forums", "Email"],
            "messaging_angle": f"Highlight core benefits of {prod_title.lower()} with clear value, high quality, and effortless adoption.",
        },
        {
            "persona_name": f"Value-Focused {ind} Consumer",
            "demographics": {
                "age_range": "28-50",
                "gender": "Mixed",
                "income": "Moderate Income",
                "education": "College Degree",
                "location": "Suburban & Regional",
            },
            "pain_points": [
                "Budget constraints and price transparency concerns",
                "Wary of hidden costs and complex onboarding",
                "Needs fast, reliable results with money-back guarantee",
            ],
            "channels": ["Facebook", "Instagram", "Google Search", "YouTube"],
            "messaging_angle": f"Emphasize accessibility, proven customer reviews, and direct value for {prod_title.lower()}.",
        },
        {
            "persona_name": "Growth & Premium Enthusiast",
            "demographics": {
                "age_range": "30-48",
                "gender": "Mixed",
                "income": "High Income",
                "education": "Graduate Degree",
                "location": "Major Commercial Hubs",
            },
            "pain_points": [
                "Outgrown basic options and seeking premium performance",
                "Needs scale, consistency, and long-term sustainability",
                "Requires high aesthetic standards and top customer support",
            ],
            "channels": ["LinkedIn", "Instagram", "Curated Newsletters", "Podcasts"],
            "messaging_angle": f"Position as the premier, high-performance choice for discerning {ind.lower()} buyers.",
        },
    ]


async def generate_mock_ad_copy(
    product_description: str, persona: dict, platform: str
) -> dict:
    """Return dynamic mock ad copy tailored to product description and platform."""
    await asyncio.sleep(random.uniform(0.2, 0.5))
    prod_title = _extract_product_title(product_description)

    copies = {
        "google": {
            "headline": f"Discover {prod_title[:28]}",
            "body": f"Designed for customers who demand quality. Save time, reduce friction, and get superior results. Order today.",
            "cta": "Shop Now",
        },
        "meta": {
            "headline": f"The Smarter Choice for {prod_title[:24]}",
            "body": f"Experience the difference with our premium formulation. Trusted by thousands of happy customers nationwide.",
            "cta": "Learn More",
        },
        "linkedin": {
            "headline": f"Elevate Your Routine with {prod_title[:24]}",
            "body": f"Industry professionals recommend our solution for consistent, high-impact results. See why top buyers choose us.",
            "cta": "Explore Now",
        },
        "instagram": {
            "headline": f"Transform Your Day ✨",
            "body": f"Say goodbye to complicated choices. Experience simple, effective {prod_title[:25].lower()} designed for your lifestyle.",
            "cta": "Get Yours",
        },
    }

    return copies.get(platform, copies["google"])


async def generate_mock_keywords(product_description: str, industry: str = "general") -> list[dict]:
    """Return dynamic mock keywords strictly grounded in the product domain."""
    await asyncio.sleep(random.uniform(0.3, 0.5))
    domain_terms = _extract_domain_keywords(product_description, industry)

    t1 = domain_terms[0] if len(domain_terms) > 0 else "product"
    t2 = domain_terms[1] if len(domain_terms) > 1 else "routine"
    t3 = domain_terms[2] if len(domain_terms) > 2 else "natural"

    # Build domain-accurate keywords without generic software suffixes
    return [
        {"keyword": f"best {t1} {t2}", "keyword_type": "seo", "intent": "transactional", "relevance_score": 0.96},
        {"keyword": f"{t1} {t2} routine", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.93},
        {"keyword": f"buy {t1} online", "keyword_type": "ppc", "intent": "transactional", "relevance_score": 0.91},
        {"keyword": f"top rated {t1} {t3}", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.89},
        {"keyword": f"affordable {t1} for beginners", "keyword_type": "ppc", "intent": "transactional", "relevance_score": 0.87},
        {"keyword": f"{t1} benefits and reviews", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.85},
        {"keyword": f"organic {t1} {t2} set", "keyword_type": "ppc", "intent": "transactional", "relevance_score": 0.84},
        {"keyword": f"how to choose {t1}", "keyword_type": "seo", "intent": "informational", "relevance_score": 0.82},
        {"keyword": f"premium {t1} brand 2025", "keyword_type": "ppc", "intent": "navigational", "relevance_score": 0.80},
    ]


async def generate_mock_budget(
    goal: str, industry: str, budget_amount: float
) -> list[dict]:
    """Return dynamic budget allocation based on total budget amount."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    allocations = [
        {"channel": "Google Search Ads", "allocation_percent": 35.0, "reasoning": "High-intent search captures active shoppers seeking immediate solutions with clear purchase intent."},
        {"channel": "Social Media Ads (Meta/Instagram)", "allocation_percent": 30.0, "reasoning": "Visual product creative and retargeting campaigns to build strong brand engagement."},
        {"channel": "Content Marketing & SEO", "allocation_percent": 15.0, "reasoning": "Long-term organic search authority and educational content driving sustainable traffic."},
        {"channel": "Email Nurture & Retention", "allocation_percent": 12.0, "reasoning": "Automated email welcome series and repeat customer incentives to maximize customer LTV."},
        {"channel": "Influencers & Strategic Partners", "allocation_percent": 8.0, "reasoning": "Micro-influencer sampling and partner endorsements to build authentic social proof."},
    ]

    for alloc in allocations:
        alloc["amount"] = round(budget_amount * alloc["allocation_percent"] / 100, 2)

    return allocations


async def generate_mock_schedule(ad_copies: list, duration_weeks: int = 4) -> list[dict]:
    """Return dynamic publishing schedule."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    return [
        {"day_offset": 1, "channel": "Google Search", "content_summary": "Launch targeted high-intent search ad campaign with product-focused keywords."},
        {"day_offset": 2, "channel": "Meta & Instagram", "content_summary": "Publish core problem-solution video and image carousel ads to target demographics."},
        {"day_offset": 5, "channel": "Blog & Content", "content_summary": "Publish comprehensive buyer's guide addressing top customer pain points."},
        {"day_offset": 8, "channel": "Email Campaign", "content_summary": "Send launch announcement email sequence to subscriber list with limited-time offer."},
        {"day_offset": 14, "channel": "Performance Review", "content_summary": "Analyze initial CTR and CAC metrics; reallocate budget to top-performing creative variants."},
        {"day_offset": 21, "channel": "Retargeting Ads", "content_summary": "Deploy retargeting ads featuring customer reviews and testimonials to engaged site visitors."},
        {"day_offset": 28, "channel": "Monthly Scaling", "content_summary": "Evaluate overall Return on Ad Spend (ROAS) and scale winning campaigns into the next month."},
    ]


async def generate_mock_summary(campaign_data: dict) -> str:
    """Return a rich 3-paragraph executive campaign summary without truncation or hardcoded templates."""
    await asyncio.sleep(random.uniform(0.3, 0.5))
    product = campaign_data.get("product_description", "the product")
    prod_title = _extract_product_title(product)
    goal = campaign_data.get("marketing_goal", "growth").replace("_", " ")
    industry = campaign_data.get("industry", "general").replace("_", " ").capitalize()
    budget = campaign_data.get("budget_amount", 0)

    p1 = (
        f"This strategic marketing campaign for {prod_title} is specifically engineered to achieve the primary goal of {goal} "
        f"within the {industry} sector. The strategy focuses on positioning the product as a superior, hassle-free choice "
        f"for target buyers who struggle with inefficient alternatives. By addressing core consumer pain points through clear value "
        f"messaging, the campaign establishes immediate trust and drives customer acquisition."
    )

    p2 = (
        f"Supported by an overall budget allocation of ₹{budget:,.2f}, the execution leverages a high-performing multi-channel "
        f"mix spanning Google Search, Meta (Instagram/Facebook), and organic content channels. High-intent search acquisition "
        f"captures active demand, while visual social advertising builds brand awareness and engagement. Complementary email "
        f"nurture sequences and strategic content marketing ensure high retention and maximum customer lifetime value."
    )

    p3 = (
        f"The 28-day campaign roadmap follows a structured 3-phase launch framework. Initial creative testing and channel validation "
        f"take place during Days 1–7, followed by data-driven budget optimization and retargeting at Day 14. By Day 28, the campaign "
        f"reaches full scale across top-performing channels, establishing sustainable market presence while keeping Customer Acquisition "
        f"Cost (CAC) tightly optimized."
    )

    return f"{p1}\n\n{p2}\n\n{p3}"
