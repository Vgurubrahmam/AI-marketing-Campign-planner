from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.middleware.auth_dependency import get_current_user
from app.models.user import User
from app.repositories.campaign_repo import CampaignRepository
from app.schemas.campaign import (
    CampaignListResponse,
    CampaignResponse,
    DashboardStatsResponse,
)

router = APIRouter()


@router.get("/campaigns", response_model=CampaignListResponse)
async def list_campaigns(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of campaigns for the current user."""
    repo = CampaignRepository(db)
    campaigns, total = await repo.get_user_campaigns(user.id, page, limit)

    return CampaignListResponse(
        campaigns=[CampaignResponse.model_validate(c) for c in campaigns],
        total=total,
    )


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard statistics for the current user."""
    repo = CampaignRepository(db)
    stats = await repo.get_user_stats(user.id)
    return DashboardStatsResponse(**stats)
