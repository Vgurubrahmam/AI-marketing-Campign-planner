from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.middleware.auth_dependency import get_current_user
from app.models.user import User
from app.repositories.campaign_repo import CampaignRepository
from app.schemas.campaign import (
    CampaignCreate,
    CampaignCreateResponse,
    CampaignResponse,
    CampaignStatusResponse,
    RegenerateRequest,
)
from app.services.campaign_service import regenerate_section, run_generation_pipeline

router = APIRouter()


@router.post("", status_code=202, response_model=CampaignCreateResponse)
async def create_campaign(
    payload: CampaignCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new campaign and start AI generation in the background."""
    repo = CampaignRepository(db)
    campaign = await repo.create(user.id, payload)
    await db.commit()

    # Kick off AI pipeline in background
    background_tasks.add_task(run_generation_pipeline, campaign.id)

    return CampaignCreateResponse(campaign_id=campaign.id, status="generating")


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a campaign with all sections."""
    repo = CampaignRepository(db)
    campaign = await repo.get_by_id(campaign_id, user.id)

    if not campaign:
        raise NotFoundError("Campaign")

    return CampaignResponse.model_validate(campaign)


@router.get("/{campaign_id}/status", response_model=CampaignStatusResponse)
async def get_campaign_status(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get campaign generation status (for polling)."""
    repo = CampaignRepository(db)
    campaign = await repo.get_by_id(campaign_id, user.id)

    if not campaign:
        raise NotFoundError("Campaign")

    return CampaignStatusResponse(
        id=campaign.id,
        status=campaign.status,
        section_status=campaign.section_status,
        created_at=campaign.created_at,
    )


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a campaign and all its sections."""
    repo = CampaignRepository(db)
    deleted = await repo.delete(campaign_id, user.id)

    if not deleted:
        raise NotFoundError("Campaign")

    return {"success": True}


@router.post("/{campaign_id}/regenerate")
async def regenerate_campaign_section(
    campaign_id: str,
    payload: RegenerateRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Regenerate a specific section of a campaign."""
    repo = CampaignRepository(db)
    campaign = await repo.get_by_id(campaign_id, user.id)

    if not campaign:
        raise NotFoundError("Campaign")

    # Kick off section regeneration in background
    background_tasks.add_task(regenerate_section, campaign.id, payload.section)

    return {"status": "regenerating", "section": payload.section}
