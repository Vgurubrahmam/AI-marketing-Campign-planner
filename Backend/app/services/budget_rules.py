"""
Deterministic budget allocation rules engine.
Numbers are computed here (not by the LLM) to prevent hallucinated budgets.
The LLM only provides strategic reasoning text via the budget prompt.
"""


# Default allocation templates by marketing goal
GOAL_ALLOCATIONS = {
    "brand_awareness": [
        {"channel": "Meta Ads (Facebook/Instagram)", "allocation_percent": 30.0},
        {"channel": "Google Ads (Display)", "allocation_percent": 20.0},
        {"channel": "LinkedIn Ads", "allocation_percent": 15.0},
        {"channel": "Content Marketing & SEO", "allocation_percent": 15.0},
        {"channel": "Influencer & Partnerships", "allocation_percent": 10.0},
        {"channel": "Email Marketing", "allocation_percent": 10.0},
    ],
    "lead_generation": [
        {"channel": "Google Ads (Search)", "allocation_percent": 30.0},
        {"channel": "Meta Ads (Facebook/Instagram)", "allocation_percent": 25.0},
        {"channel": "LinkedIn Ads", "allocation_percent": 15.0},
        {"channel": "Content Marketing & SEO", "allocation_percent": 15.0},
        {"channel": "Email Marketing", "allocation_percent": 10.0},
        {"channel": "Influencer & Partnerships", "allocation_percent": 5.0},
    ],
    "sales": [
        {"channel": "Google Ads (Search)", "allocation_percent": 35.0},
        {"channel": "Meta Ads (Facebook/Instagram)", "allocation_percent": 25.0},
        {"channel": "Email Marketing", "allocation_percent": 15.0},
        {"channel": "Content Marketing & SEO", "allocation_percent": 10.0},
        {"channel": "LinkedIn Ads", "allocation_percent": 10.0},
        {"channel": "Influencer & Partnerships", "allocation_percent": 5.0},
    ],
    "engagement": [
        {"channel": "Meta Ads (Facebook/Instagram)", "allocation_percent": 30.0},
        {"channel": "Content Marketing & SEO", "allocation_percent": 20.0},
        {"channel": "Influencer & Partnerships", "allocation_percent": 20.0},
        {"channel": "Email Marketing", "allocation_percent": 15.0},
        {"channel": "Google Ads (Search)", "allocation_percent": 10.0},
        {"channel": "LinkedIn Ads", "allocation_percent": 5.0},
    ],
}

# Industry-specific adjustments (modify allocation_percent deltas)
INDUSTRY_ADJUSTMENTS = {
    "technology": {"LinkedIn Ads": +5, "Influencer & Partnerships": -5},
    "ecommerce": {"Google Ads (Search)": +5, "LinkedIn Ads": -5},
    "healthcare": {"Content Marketing & SEO": +5, "Influencer & Partnerships": -5},
    "finance": {"Google Ads (Search)": +5, "Meta Ads (Facebook/Instagram)": -5},
    "education": {"Content Marketing & SEO": +5, "Google Ads (Search)": -5},
    "saas": {"Google Ads (Search)": +5, "Influencer & Partnerships": -5},
    "retail": {"Meta Ads (Facebook/Instagram)": +5, "LinkedIn Ads": -5},
}


def compute_budget_allocation(
    goal: str, industry: str, budget_amount: float
) -> list[dict]:
    """
    Compute deterministic budget allocations based on goal and industry.

    Returns a list of dicts with channel, allocation_percent, and amount.
    """
    # Get base allocation for goal (default to lead_generation)
    goal_key = goal.lower().replace(" ", "_")
    base_allocations = GOAL_ALLOCATIONS.get(goal_key, GOAL_ALLOCATIONS["lead_generation"])

    # Deep copy to avoid mutating the template
    allocations = [dict(a) for a in base_allocations]

    # Apply industry adjustments
    industry_key = industry.lower().replace(" ", "_")
    adjustments = INDUSTRY_ADJUSTMENTS.get(industry_key, {})

    for alloc in allocations:
        delta = adjustments.get(alloc["channel"], 0)
        alloc["allocation_percent"] = max(
            5.0, min(50.0, alloc["allocation_percent"] + delta)
        )

    # Normalize to 100%
    total_percent = sum(a["allocation_percent"] for a in allocations)
    for alloc in allocations:
        alloc["allocation_percent"] = round(
            alloc["allocation_percent"] / total_percent * 100, 2
        )
        alloc["amount"] = round(
            budget_amount * alloc["allocation_percent"] / 100, 2
        )

    return allocations
