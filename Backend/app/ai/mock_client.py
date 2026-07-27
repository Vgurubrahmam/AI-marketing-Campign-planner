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


def format_currency_inr(amount: float) -> str:
    """Format float amount into Indian currency format (e.g., ₹5,00,000)."""
    val = int(round(amount))
    s = str(val)
    if len(s) <= 3:
        return f"₹{s}"
    last_three = s[-3:]
    other = s[:-3]
    parts = []
    while len(other) > 2:
        parts.insert(0, other[-2:])
        other = other[:-2]
    if other:
        parts.insert(0, other)
    return f"₹{','.join(parts)},{last_three}"


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
    domain_terms = _extract_domain_keywords(product_description, industry)
    dt1 = domain_terms[0].capitalize() if domain_terms else "Quality"
    dt2 = domain_terms[1].capitalize() if len(domain_terms) > 1 else "Convenient"

    prod_lower = product_description.lower()
    if "clean" in prod_lower or "home" in prod_lower or "house" in prod_lower:
        p1_name = "Eco-Conscious Parent"
        p2_name = "Busy Professional"
        p3_name = "Health-Conscious Homeowner"
    elif "skin" in prod_lower or "beauty" in prod_lower or "cosmetic" in prod_lower:
        p1_name = "Minimalist Beauty Buyer"
        p2_name = "Sensitive-Skin Shopper"
        p3_name = "Busy Lifestyle Consumer"
    elif "freelanc" in prod_lower or "tax" in prod_lower or "finance" in prod_lower or "expense" in prod_lower:
        p1_name = "Independent Contractor"
        p2_name = "Freelance Consultant"
        p3_name = "Solopreneur Founder"
    else:
        p1_name = f"Eco-{dt1} Buyer"
        p2_name = f"Busy {dt2} User"
        p3_name = f"Value-Driven Consumer"

    return [
        {
            "persona_name": p1_name,
            "demographics": {
                "age_range": "25-42",
                "gender": "Female / Diverse",
                "income": "₹6,00,000 - ₹10,00,000 / year",
                "education": "Bachelor's Degree",
                "location": "Metro & Urban areas",
            },
            "pain_points": [
                f"Overwhelmed by complex options for {prod_title.lower()}",
                "Needs a fast, reliable solution without extra hassle",
                "Demands safety, quality standards, and transparent pricing",
            ],
            "channels": ["Instagram", "Google Ads (Search)", "Content Marketing & SEO", "Email Marketing"],
            "messaging_angle": f"Highlight simplicity, safety, and guaranteed quality for {prod_title.lower()}.",
        },
        {
            "persona_name": p2_name,
            "demographics": {
                "age_range": "28-48",
                "gender": "Male / Diverse",
                "income": "₹8,00,000 - ₹15,00,000 / year",
                "education": "College Degree",
                "location": "Suburban & Urban",
            },
            "pain_points": [
                f"Lack of time to handle {prod_title.lower()} independently",
                "Wants straightforward service delivering consistent results",
                "Demands transparent pricing without hidden fees",
            ],
            "channels": ["Google Ads (Search)", "YouTube", "Content Marketing & SEO", "Meta Ads (Facebook/Instagram)"],
            "messaging_angle": f"Emphasize time-saving convenience and verified customer results for {prod_title.lower()}.",
        },
        {
            "persona_name": p3_name,
            "demographics": {
                "age_range": "30-52",
                "gender": "Diverse",
                "income": "₹12,00,000+ / year",
                "education": "Graduate Degree",
                "location": "Major Urban Centers",
            },
            "pain_points": [
                f"Seeking premium, hassle-free solutions for {prod_title.lower()}",
                "Requires flexible scheduling or subscription options",
                "Values sustainable and non-toxic standards",
            ],
            "channels": ["Meta Ads (Facebook/Instagram)", "LinkedIn Ads", "Email Marketing"],
            "messaging_angle": f"Focus on premium quality, reliability, and subscription convenience for {prod_title.lower()}.",
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


async def generate_mock_schedule(
    product_description: str = "", personas_summary: str = "", goal: str = "growth"
) -> list[dict]:
    """Return dynamic publishing schedule using current campaign's product and personas."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    prod_title = _extract_product_title(product_description) if product_description else "the product"

    persona_names = []
    if personas_summary:
        parts = [p.strip() for p in personas_summary.split(",") if p.strip()]
        persona_names = [p.split(":")[0].strip() for p in parts if p.strip()]

    p1 = persona_names[0] if len(persona_names) > 0 else "Primary Persona"
    p2 = persona_names[1] if len(persona_names) > 1 else "Secondary Persona"
    p3 = persona_names[2] if len(persona_names) > 2 else "Target Audience"

    return [
        {"day_offset": 1, "channel": "Google Search Ads", "content_summary": f"Launch targeted Google Search ads for '{prod_title}' focusing on high-intent search terms. Target CPC under ₹80."},
        {"day_offset": 2, "channel": "Meta Ads (Facebook/Instagram)", "content_summary": f"Publish core problem-solution video carousel targeting {p1} and {p2} highlighting key product benefits."},
        {"day_offset": 5, "channel": "Content Marketing & SEO", "content_summary": f"Publish comprehensive buyer's guide addressing top customer pain points for {p1}."},
        {"day_offset": 8, "channel": "Email Marketing", "content_summary": f"Send launch announcement email sequence for '{prod_title}' to subscriber list with exclusive subscriber offer."},
        {"day_offset": 14, "channel": "Performance Checkpoint", "content_summary": f"Analyze initial CTR and CAC metrics for '{prod_title}'; reallocate budget to top-performing ad creative variants."},
        {"day_offset": 21, "channel": "Retargeting Ads", "content_summary": f"Deploy retargeting ads targeting {p3} featuring verified customer reviews and social proof."},
        {"day_offset": 28, "channel": "Campaign Scaling", "content_summary": f"Evaluate overall Return on Ad Spend (ROAS) in INR and scale winning ad sets for '{prod_title}' into the next phase."},
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

    budget_formatted = format_currency_inr(budget)

    p2_openers = [
        f"Capitalizing on an overall campaign budget of {budget_formatted}, funds are allocated strategically across top acquisition channels including {channel_str}.",
        f"With a total investment of {budget_formatted}, the multi-channel acquisition model prioritizes high-performing platforms led by {channel_str}.",
        f"Backed by a structured budget of {budget_formatted}, execution is focused on high-yielding channels including {channel_str}.",
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


async def generate_mock_trending_keywords(product_description: str, industry: str = "general") -> list[dict]:
    """Return dynamic mock trending keywords with rationale."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    domain_terms = _extract_domain_keywords(product_description, industry)
    t1 = domain_terms[0] if len(domain_terms) > 0 else "smart"
    t2 = domain_terms[1] if len(domain_terms) > 1 else "solution"

    return [
        {
            "keyword": f"eco-friendly {t1} trends 2025",
            "reason": f"Spike in consumer interest for sustainable and non-toxic {t1} alternatives.",
        },
        {
            "keyword": f"AI-powered {t2} tools",
            "reason": f"High search velocity around automation and smart productivity tools in {industry}.",
        },
        {
            "keyword": f"best affordable {t1} for urban lifestyle",
            "reason": f"Growing demand among metro consumers for cost-effective, high-quality {t1} products.",
        },
        {
            "keyword": f"top rated {t1} reviews",
            "reason": f"Viral social media discussions comparing leading brands in the {industry} market.",
        },
    ]


async def generate_mock_competitors(product_description: str, industry: str = "general") -> list[dict]:
    """Return dynamic mock competitors with positioning and differentiator opportunities."""
    await asyncio.sleep(random.uniform(0.2, 0.4))
    ind = industry.replace('_', ' ').capitalize()
    prod_title = _extract_product_title(product_description)

    return [
        {
            "name": f"BrandX {ind}",
            "positioning": f"Legacy market leader offering broad {ind.lower()} solutions with high premium pricing.",
            "differentiator_opportunity": f"Undersell on price while offering faster onboarding and modern features for '{prod_title}'.",
        },
        {
            "name": f"Nova{ind} Solutions",
            "positioning": f"Fast-growing D2C startup focused heavily on social media influencer marketing.",
            "differentiator_opportunity": f"Highlight verified customer trust, superior product safety, and lifetime value.",
        },
        {
            "name": f"Apex {ind} Group",
            "positioning": "B2B enterprise provider with rigid enterprise sales cycles.",
            "differentiator_opportunity": "Provide self-serve instant access, transparent INR pricing, and no long-term contracts.",
        },
    ]

