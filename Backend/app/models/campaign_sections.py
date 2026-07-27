import uuid

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class AudiencePersona(Base):
    __tablename__ = "audience_personas"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    persona_name: Mapped[str] = mapped_column(String(255), nullable=False)
    demographics: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    pain_points: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    channels: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    messaging_angle: Mapped[str] = mapped_column(Text, nullable=True)

    campaign = relationship("Campaign", back_populates="personas")


class AdCopy(Base):
    __tablename__ = "ad_copies"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    headline: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    cta: Mapped[str] = mapped_column(String(255), nullable=False)

    campaign = relationship("Campaign", back_populates="ad_copies")


class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    keyword_type: Mapped[str] = mapped_column(String(20), nullable=False)  # seo | ppc
    intent: Mapped[str] = mapped_column(
        String(50), nullable=True
    )  # informational | transactional | navigational
    relevance_score: Mapped[float] = mapped_column(Numeric(3, 2), nullable=True)

    campaign = relationship("Campaign", back_populates="keywords")


class BudgetAllocation(Base):
    __tablename__ = "budgets"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    allocation_percent: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    reasoning: Mapped[str] = mapped_column(Text, nullable=True)

    campaign = relationship("Campaign", back_populates="budgets")


class PublishingPlan(Base):
    __tablename__ = "publishing_plans"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    day_offset: Mapped[int] = mapped_column(Integer, nullable=False)
    channel: Mapped[str] = mapped_column(String(100), nullable=False)
    content_summary: Mapped[str] = mapped_column(Text, nullable=False)

    campaign = relationship("Campaign", back_populates="publishing_plans")


class TrendingKeyword(Base):
    __tablename__ = "trending_keywords"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    campaign = relationship("Campaign", back_populates="trending_keywords")


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    campaign_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("campaigns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    positioning: Mapped[str] = mapped_column(Text, nullable=False)
    differentiator_opportunity: Mapped[str] = mapped_column(Text, nullable=False)

    campaign = relationship("Campaign", back_populates="competitors")

