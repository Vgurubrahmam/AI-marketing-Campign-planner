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
    await asyncio.sleep(random.uniform(0.3, 0.5))
    prod_title = _extract_product_title(product_description)
    ind = industry.replace('_', ' ').capitalize()

    return [
        {
            "persona_name": f"Simple Sarah",
            "demographics": {
                "age_range": "25-42",
                "gender": "Female",
                "income": "Mid to High Income",
                "education": "Bachelor's Degree",
                "location": "Metro & Urban areas",
            },
            "pain_points": [
                f"Overwhelmed by complex options for {prod_title.lower()}",
                "Needs a fast, 3-step streamlined routine without clutter",
                "Concerned about product safety and gentle ingredients",
            ],
            "channels": ["Instagram", "Google Search", "Pinterest", "Email"],
            "messaging_angle": f"Highlight 3-step simplicity and clean ingredients for {prod_title.lower()}.",
        },
        {
            "persona_name": f"Mindful Mike",
            "demographics": {
                "age_range": "28-48",
                "gender": "Male",
                "income": "Moderate to High Income",
                "education": "College Degree",
                "location": "Suburban & Urban",
            },
            "pain_points": [
                "Sensitive skin irritation from harsh commercial products",
                "Wants straightforward skincare that delivers consistent results",
                "Demands clear product value without hype",
            ],
            "channels": ["Google Search", "YouTube", "Reddit", "Facebook"],
            "messaging_angle": f"Emphasize gentle formulation and dermatologist-backed results for {prod_title.lower()}.",
        },
        {
            "persona_name": "Busy Becca",
            "demographics": {
                "age_range": "30-52",
                "gender": "Female",
                "income": "High Income",
                "education": "Graduate Degree",
                "location": "Major Urban Centers",
            },
            "pain_points": [
                "Zero time for multi-step beauty routines",
                "Seeking high-performance skincare that fits active lifestyle",
                "Needs subscription convenience and fast delivery",
            ],
            "channels": ["Instagram", "LinkedIn", "Podcasts", "Email"],
            "messaging_angle": f"Focus on time-saving efficiency and subscription convenience for {prod_title.lower()}.",
        },
    ]


async def generate_mock_ad_copy(
    product_description: str, persona: dict, platform: str
) -> dict:
    """Return dynamic mock ad copy tailored to product description and platform."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    prod_title = _extract_product_title(product_description)

    copies = {
        "google": {
            "headline": f"Discover {prod_title[:28]}",
            "body": f"Designed for customers who demand quality. Save time, reduce friction, and get superior results. Order today.",
            "cta": "Shop Now",
        },
        "meta": {
            "headline": f"The Smarter Choice for {prod_title[:24]}",
            "body": f"Experience the difference with our clean formulation. Trusted by thousands of happy customers nationwide.",
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
    await asyncio.sleep(random.uniform(0.2, 0.4))
    domain_terms = _extract_domain_keywords(product_description, industry)

    t1 = domain_terms[0] if len(domain_terms) > 0 else "product"
    t2 = domain_terms[1] if len(domain_terms) > 1 else "routine"
    t3 = domain_terms[2] if len(domain_terms) > 2 else "natural"

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
    """Return dynamic publishing schedule with strict INR currency and exact persona names."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    return [
        {"day_offset": 1, "channel": "Google Search", "content_summary": "Launch targeted Google Search ads focusing on high-intent terms. Target CPC under ₹80."},
        {"day_offset": 2, "channel": "Meta & Instagram", "content_summary": "Publish core problem-solution video carousel targeting Simple Sarah and Mindful Mike."},
        {"day_offset": 5, "channel": "Blog & Content", "content_summary": "Publish comprehensive routine guide addressing sensitive skin pain points."},
        {"day_offset": 8, "channel": "Email Campaign", "content_summary": "Send launch announcement email sequence with exclusive subscriber discount."},
        {"day_offset": 14, "channel": "Performance Review", "content_summary": "Analyze initial CTR and CAC metrics; reallocate budget to top-performing ad variants."},
        {"day_offset": 21, "channel": "Retargeting Ads", "content_summary": "Deploy retargeting ads targeting Busy Becca with verified customer reviews."},
        {"day_offset": 28, "channel": "Monthly Scaling", "content_summary": "Evaluate overall Return on Ad Spend (ROAS) in INR and scale winning campaigns into the next month."},
    ]


async def generate_mock_summary(campaign_data: dict) -> str:
    """Return a fully dynamic 3-paragraph executive campaign summary synthesized with varied sentence structures."""
    await asyncio.sleep(random.uniform(0.3, 0.5))
    product = campaign_data.get("product_description", "the product")
    prod_title = _extract_product_title(product)
    goal = campaign_data.get("marketing_goal", "growth").replace("_", " ")
    industry = campaign_data.get("industry", "general").replace("_", " ").capitalize()
    budget = float(campaign_data.get("budget_amount", 0))

    # Dynamic extraction of section content
    personas = campaign_data.get("personas", [])
    persona_names = [p.get("persona_name", "") for p in personas if isinstance(p, dict) and p.get("persona_name")]
    persona_str = ", ".join(persona_names[:2]) if persona_names else "core customer segments"

    keywords = campaign_data.get("keywords", [])
    keyword_terms = [k.get("keyword", "") for k in keywords if isinstance(k, dict) and k.get("keyword")]
    keyword_str = ", ".join(f"'{k}'" for k in keyword_terms[:3]) if keyword_terms else f"high-intent search terms"

    budgets = campaign_data.get("budget_allocation", [])
    top_channels = [b.get("channel", "") for b in budgets if isinstance(b, dict) and b.get("channel")]
    channel_str = ", ".join(top_channels[:3]) if top_channels else "Google Search, Meta Ads, and Content Marketing"

    # Multiple sentence variant pools for dynamic phrasing
    p1_openers = [
        f"Designed specifically for the {industry} sector, this comprehensive campaign for '{prod_title}' focuses on driving {goal}.",
        f"This strategic marketing initiative positions '{prod_title}' to capture market leadership in {industry} with a focus on {goal}.",
        f"Focusing on the primary objective of {goal}, this strategic campaign for '{prod_title}' targets key opportunities in {industry}.",
    ]
    p1_bodies = [
        f"By addressing specific friction points faced by {persona_str}, the messaging establishes clear brand differentiation and consumer trust.",
        f"Tailored around the distinct needs of {persona_str}, the positioning highlights superior value, reliability, and effortless adoption.",
        f"Engaging core audience personas such as {persona_str}, the strategic narrative emphasizes high quality and immediate problem resolution.",
    ]

    p2_openers = [
        f"Capitalizing on an overall campaign budget of ₹{budget:,.2f}, funds are allocated strategically across top acquisition channels including {channel_str}.",
        f"With a total investment of ₹{budget:,.2f}, the multi-channel acquisition model prioritizes high-performing platforms led by {channel_str}.",
        f"Backed by a structured budget of ₹{budget:,.2f}, execution is focused on high-yielding channels including {channel_str}.",
    ]
    p2_bodies = [
        f"High-intent search capture targets keywords such as {keyword_str}, while visual social advertising builds active brand engagement and funnel velocity.",
        f"Targeted search ads focus on core terms including {keyword_str}, supported by social media campaigns that cultivate audience interest and repeat visits.",
        f"Organic and paid search campaigns prioritize search intent around {keyword_str}, while retargeting sequences maintain high conversion efficiency.",
    ]

    p3_openers = [
        f"The 28-day campaign execution roadmap is structured into three distinct performance phases.",
        f"A 28-day phased implementation plan ensures continuous optimization and scalable acquisition.",
        f"Execution unfolds over a 28-day performance roadmap designed for rapid testing and scaling.",
    ]
    p3_bodies = [
        f"Initial creative validation during Days 1–7 feeds into mid-campaign budget reallocation at Day 14, culminating in aggressive scaling through Day 28 to ensure optimal ROAS for '{prod_title}'.",
        f"Days 1–7 establish baseline metrics, followed by Day 14 optimization checkpoints and full campaign scaling by Day 28 to maximize ROI for '{prod_title}'.",
        f"Early testing in Week 1 leads to strategic budget adjustments at Day 14, scaling high-converting creative assets through Day 28 for '{prod_title}'.",
    ]

    # Randomly select variants so no two calls produce identical connective phrasing
    p1 = f"{random.choice(p1_openers)} {random.choice(p1_bodies)}"
    p2 = f"{random.choice(p2_openers)} {random.choice(p2_bodies)}"
    p3 = f"{random.choice(p3_openers)} {random.choice(p3_bodies)}"

    return f"{p1}\n\n{p2}\n\n{p3}"
