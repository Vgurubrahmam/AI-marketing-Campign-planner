from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, campaigns, dashboard
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Import all models so SQLAlchemy knows about them when creating tables
from app.models import (  # noqa: F401
    AdCopy,
    AudiencePersona,
    BudgetAllocation,
    Campaign,
    Competitor,
    Keyword,
    PublishingPlan,
    TrendingKeyword,
    User,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup (dev convenience; use Alembic in production)."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("INFO: Database tables initialized successfully.")
    except Exception as e:
        print(f"ERROR: Database startup initialization failed: {e}")
    yield


app = FastAPI(
    title="AI Marketing Campaign Planner",
    description="AI-powered marketing campaign generation API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
