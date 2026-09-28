from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import (
    activity_runs,
    children,
    events,
    health,
    media,
    onboarding,
    plans,
    profile,
    scoring,
    sessions,
    today,
)
from app.storage import ensure_bucket_exists


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    ensure_bucket_exists()
    yield


app = FastAPI(title="Learning Ecosystem API", version="0.1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(events.router)
app.include_router(profile.router)
app.include_router(plans.router)
app.include_router(scoring.router)
app.include_router(onboarding.router)
app.include_router(children.router)
app.include_router(sessions.router)
app.include_router(activity_runs.router)
app.include_router(today.router)
app.include_router(media.router)
