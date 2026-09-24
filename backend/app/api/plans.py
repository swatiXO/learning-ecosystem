from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.plan_engine.service import current_plan, replace_active_plan, serialize_plan
from app.schemas.plans import PlanOut, PlanOverrideIn

router = APIRouter(tags=["plans"])


@router.get("/children/{child_id}/plan", response_model=PlanOut)
def get_plan(child_id: UUID, db: Session = Depends(get_db)) -> PlanOut:
    plan = current_plan(db, child_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active plan for this child")
    return serialize_plan(db, plan)


@router.put("/children/{child_id}/plan", response_model=PlanOut)
def override_plan(
    child_id: UUID, override: PlanOverrideIn, db: Session = Depends(get_db)
) -> PlanOut:
    # Rule #8: plan overrides require a human action and must be logged. This endpoint IS
    # that human action; created_by="therapist" plus created_at is the log entry.
    modules = {module.module: module.weight for module in override.modules}
    plan = replace_active_plan(
        db, child_id, modules=modules, rationale=override.rationale, created_by="therapist"
    )
    db.commit()
    db.refresh(plan)
    return serialize_plan(db, plan)
