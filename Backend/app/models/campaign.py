import uuid
import json
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def default_section_status() -> dict:
    return {
        "persona": "pending",
        "ad_copy": "pending",
        "keywords": "pending",
        "budget": "pending",
        "schedule": "pending",
        "summary": "pending",
    }


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_description: Mapped[str] = mapped_column(Text, nullable=False)
    marketing_goal: Mapped[str] = mapped_column(String(100), nullable=False)
    industry: Mapped[str] = mapped_column(String(100), nullable=False)
    budget_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="generating"
    )
    # Tracks per-section generation progress (stored as JSON)
    section_status: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=default_section_status,
    )
    # AI-generated executive summary text
    summary: Mapped[str] = mapped_column(Text, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user = relationship("User", back_populates="campaigns")
    personas = relationship(
        "AudiencePersona", back_populates="campaign", cascade="all, delete-orphan"
    )
    ad_copies = relationship(
        "AdCopy", back_populates="campaign", cascade="all, delete-orphan"
    )
    keywords = relationship(
        "Keyword", back_populates="campaign", cascade="all, delete-orphan"
    )
    budgets = relationship(
        "BudgetAllocation", back_populates="campaign", cascade="all, delete-orphan"
    )
    publishing_plans = relationship(
        "PublishingPlan", back_populates="campaign", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_campaigns_user_created", "user_id", "created_at"),
    )
