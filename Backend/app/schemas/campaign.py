from datetime import datetime

from pydantic import BaseModel, Field


# --- Request schemas ---


class CampaignCreate(BaseModel):
    product_description: str = Field(
        ..., min_length=20, max_length=5000, description="Detailed product/service description"
    )
    marketing_goal: str = Field(
        ..., min_length=1, max_length=100, description="e.g. brand_awareness, lead_generation, sales"
    )
    industry: str = Field(
        ..., min_length=1, max_length=100, description="e.g. technology, healthcare, ecommerce"
    )
    budget_amount: float = Field(
        ..., gt=0, le=1_000_000_000, description="Total campaign budget in INR"
    )


class RegenerateRequest(BaseModel):
    section: str = Field(
        ..., pattern="^(persona|ad_copy|keywords|budget|schedule|summary)$"
    )


# --- Section response schemas ---


class PersonaResponse(BaseModel):
    id: str
    persona_name: str
    demographics: dict
    pain_points: list
    channels: list
    messaging_angle: str | None

    model_config = {"from_attributes": True}


class AdCopyResponse(BaseModel):
    id: str
    platform: str
    headline: str
    body: str
    cta: str

    model_config = {"from_attributes": True}


class KeywordResponse(BaseModel):
    id: str
    keyword: str
    keyword_type: str
    intent: str | None
    relevance_score: float | None

    model_config = {"from_attributes": True}


class BudgetResponse(BaseModel):
    id: str
    channel: str
    allocation_percent: float
    amount: float
    reasoning: str | None

    model_config = {"from_attributes": True}


class PublishingPlanResponse(BaseModel):
    id: str
    day_offset: int
    channel: str
    content_summary: str

    model_config = {"from_attributes": True}


# --- Campaign response schemas ---


class CampaignStatusResponse(BaseModel):
    id: str
    status: str
    section_status: dict
    created_at: datetime


class CampaignResponse(BaseModel):
    id: str
    product_description: str
    marketing_goal: str
    industry: str
    budget_amount: float
    status: str
    section_status: dict
    created_at: datetime
    personas: list[PersonaResponse] = []
    ad_copies: list[AdCopyResponse] = []
    keywords: list[KeywordResponse] = []
    budgets: list[BudgetResponse] = []
    publishing_plans: list[PublishingPlanResponse] = []
    summary: str | None = None

    model_config = {"from_attributes": True}


class CampaignListResponse(BaseModel):
    campaigns: list[CampaignResponse]
    total: int


class CampaignCreateResponse(BaseModel):
    campaign_id: str
    status: str = "generating"


class DashboardStatsResponse(BaseModel):
    total_campaigns: int
    this_month: int
    generating: int
    completed: int
