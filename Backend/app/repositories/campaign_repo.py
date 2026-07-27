from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.campaign import Campaign
from app.models.campaign_sections import (
    AdCopy,
    AudiencePersona,
    BudgetAllocation,
    Competitor,
    Keyword,
    PublishingPlan,
    TrendingKeyword,
)
from app.schemas.campaign import CampaignCreate


class CampaignRepository:
    """Handles all database operations for campaigns and their sections."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: str, data: CampaignCreate) -> Campaign:
        campaign = Campaign(
            user_id=str(user_id),
            product_description=data.product_description,
            marketing_goal=data.marketing_goal,
            industry=data.industry,
            budget_amount=data.budget_amount,
            status="generating",
        )
        self.db.add(campaign)
        await self.db.flush()
        await self.db.refresh(campaign)
        return campaign

    async def get_by_id(
        self, campaign_id: str, user_id: Optional[str] = None
    ) -> Optional[Campaign]:
        query = (
            select(Campaign)
            .options(
                selectinload(Campaign.personas),
                selectinload(Campaign.ad_copies),
                selectinload(Campaign.keywords),
                selectinload(Campaign.trending_keywords),
                selectinload(Campaign.competitors),
                selectinload(Campaign.budgets),
                selectinload(Campaign.publishing_plans),
            )
            .where(Campaign.id == str(campaign_id))
        )
        if user_id:
            query = query.where(Campaign.user_id == str(user_id))

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_campaigns(
        self, user_id: str, page: int = 1, limit: int = 10
    ) -> tuple[list[Campaign], int]:
        # Get total count
        count_query = (
            select(func.count(Campaign.id))
            .where(Campaign.user_id == str(user_id))
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar_one()

        # Get paginated campaigns
        offset = (page - 1) * limit
        query = (
            select(Campaign)
            .options(
                selectinload(Campaign.personas),
                selectinload(Campaign.ad_copies),
                selectinload(Campaign.keywords),
                selectinload(Campaign.trending_keywords),
                selectinload(Campaign.competitors),
                selectinload(Campaign.budgets),
                selectinload(Campaign.publishing_plans),
            )
            .where(Campaign.user_id == str(user_id))
            .order_by(desc(Campaign.created_at))
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(query)
        campaigns = list(result.scalars().all())

        return campaigns, total

    async def get_user_stats(self, user_id: str) -> dict:
        now = datetime.now(timezone.utc)
        first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        uid = str(user_id)

        # Total campaigns
        total_result = await self.db.execute(
            select(func.count(Campaign.id)).where(Campaign.user_id == uid)
        )
        total = total_result.scalar_one()

        # This month
        month_result = await self.db.execute(
            select(func.count(Campaign.id)).where(
                Campaign.user_id == uid,
                Campaign.created_at >= first_of_month,
            )
        )
        this_month = month_result.scalar_one()

        # By status
        generating_result = await self.db.execute(
            select(func.count(Campaign.id)).where(
                Campaign.user_id == uid,
                Campaign.status == "generating",
            )
        )
        generating = generating_result.scalar_one()

        completed_result = await self.db.execute(
            select(func.count(Campaign.id)).where(
                Campaign.user_id == uid,
                Campaign.status == "complete",
            )
        )
        completed = completed_result.scalar_one()

        return {
            "total_campaigns": total,
            "this_month": this_month,
            "generating": generating,
            "completed": completed,
        }

    async def update_section_status(
        self, campaign_id: str, section: str, status: str
    ) -> None:
        campaign = await self.db.get(Campaign, str(campaign_id))
        if campaign:
            section_status = dict(campaign.section_status)
            section_status[section] = status
            campaign.section_status = section_status
            await self.db.flush()

    async def update_campaign_status(
        self, campaign_id: str, status: str
    ) -> None:
        campaign = await self.db.get(Campaign, str(campaign_id))
        if campaign:
            campaign.status = status
            await self.db.flush()

    async def update_summary(self, campaign_id: str, summary: str) -> None:
        campaign = await self.db.get(Campaign, str(campaign_id))
        if campaign:
            campaign.summary = summary
            await self.db.flush()

    async def delete(self, campaign_id: str, user_id: str) -> bool:
        campaign = await self.db.get(Campaign, str(campaign_id))
        if campaign and campaign.user_id == str(user_id):
            await self.db.delete(campaign)
            await self.db.flush()
            return True
        return False

    # --- Section CRUD ---

    async def add_personas(self, campaign_id: str, personas: list[dict]) -> list[AudiencePersona]:
        models = []
        for p in personas:
            model = AudiencePersona(
                campaign_id=str(campaign_id),
                persona_name=p.get("persona_name", "Unnamed Persona"),
                demographics=p.get("demographics", {}),
                pain_points=p.get("pain_points", []),
                channels=p.get("channels", []),
                messaging_angle=p.get("messaging_angle"),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_ad_copies(self, campaign_id: str, copies: list[dict]) -> list[AdCopy]:
        models = []
        for c in copies:
            model = AdCopy(
                campaign_id=str(campaign_id),
                platform=c.get("platform", "unknown"),
                headline=c.get("headline", ""),
                body=c.get("body", ""),
                cta=c.get("cta", ""),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_keywords(self, campaign_id: str, keywords: list[dict]) -> list[Keyword]:
        models = []
        for k in keywords:
            model = Keyword(
                campaign_id=str(campaign_id),
                keyword=k.get("keyword", ""),
                keyword_type=k.get("keyword_type", "seo"),
                intent=k.get("intent"),
                relevance_score=k.get("relevance_score"),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_budgets(self, campaign_id: str, budgets: list[dict]) -> list[BudgetAllocation]:
        models = []
        for b in budgets:
            model = BudgetAllocation(
                campaign_id=str(campaign_id),
                channel=b.get("channel", ""),
                allocation_percent=b.get("allocation_percent", 0),
                amount=b.get("amount", 0),
                reasoning=b.get("reasoning"),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_publishing_plans(self, campaign_id: str, plans: list[dict]) -> list[PublishingPlan]:
        models = []
        for p in plans:
            model = PublishingPlan(
                campaign_id=str(campaign_id),
                day_offset=p.get("day_offset", 1),
                channel=p.get("channel", ""),
                content_summary=p.get("content_summary", ""),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_trending_keywords(self, campaign_id: str, keywords: list[dict]) -> list[TrendingKeyword]:
        models = []
        for k in keywords:
            model = TrendingKeyword(
                campaign_id=str(campaign_id),
                keyword=k.get("keyword", ""),
                reason=k.get("reason", ""),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def add_competitors(self, campaign_id: str, competitors: list[dict]) -> list[Competitor]:
        models = []
        for c in competitors:
            model = Competitor(
                campaign_id=str(campaign_id),
                name=c.get("name", ""),
                positioning=c.get("positioning", ""),
                differentiator_opportunity=c.get("differentiator_opportunity", ""),
            )
            self.db.add(model)
            models.append(model)
        await self.db.flush()
        return models

    async def clear_section(self, campaign_id: str, section: str) -> None:
        """Delete all records for a specific section of a campaign (for regeneration)."""
        model_map = {
            "persona": AudiencePersona,
            "ad_copy": AdCopy,
            "keywords": Keyword,
            "trending": TrendingKeyword,
            "competitors": Competitor,
            "budget": BudgetAllocation,
            "schedule": PublishingPlan,
        }
        model_class = model_map.get(section)
        if model_class:
            result = await self.db.execute(
                select(model_class).where(model_class.campaign_id == str(campaign_id))
            )
            for record in result.scalars().all():
                await self.db.delete(record)
            await self.db.flush()

