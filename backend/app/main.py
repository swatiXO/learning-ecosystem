from fastapi import FastAPI

from app.api import events, health, plans, profile

app = FastAPI(title="Learning Ecosystem API", version="0.1.0")

app.include_router(health.router)
app.include_router(events.router)
app.include_router(profile.router)
app.include_router(plans.router)

# Each track adds its own router here as it lands, e.g.:
# from app.api import onboarding
# app.include_router(onboarding.router)
