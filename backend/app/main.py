from fastapi import FastAPI

from app.api import (
    activity_runs,
    children,
    events,
    health,
    onboarding,
    plans,
    profile,
    scoring,
    sessions,
)

app = FastAPI(title="Learning Ecosystem API", version="0.1.0")

app.include_router(health.router)
app.include_router(events.router)
app.include_router(profile.router)
app.include_router(plans.router)
app.include_router(scoring.router)
app.include_router(onboarding.router)
app.include_router(children.router)
app.include_router(sessions.router)
app.include_router(activity_runs.router)
