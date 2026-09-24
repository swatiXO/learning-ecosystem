from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Plan, PlanModule
from app.schemas.plans import PlanModuleOut, PlanOut, PlanOverrideIn

router = APIRouter(tags=["plans"])


def _current_plan(db: Session, child_id: UUID) -> Plan | None:
    return db.scalar(
        select(Plan)
        .where(Plan.child_id == child_id, Plan.status == "active")
        .order_by(Plan.version.desc())
    )


def _serialize_plan(db: Session, plan: Plan) -> PlanOut:
    modules = db.scalars(select(PlanModule).where(PlanModule.plan_id == plan.id)).all()
    return PlanOut(
        id=plan.id,
        child_id=plan.child_id,
        version=plan.version,
        status=plan.status,
        rationale=plan.rationale,
        created_by=plan.created_by,
        created_at=plan.created_at,
        modules=[PlanModuleOut(module=m.module, weight=m.weight) for m in modules],
    )


@router.get("/children/{child_id}/plan", response_model=PlanOut)
def get_plan(child_id: UUID, db: Session = Depends(get_db)) -> PlanOut:
    plan = _current_plan(db, child_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active plan for this child")
    return _serialize_plan(db, plan)


@router.put("/children/{child_id}/plan", response_model=PlanOut)
def override_plan(
    child_id: UUID, override: PlanOverrideIn, db: Session = Depends(get_db)
) -> PlanOut:
    # Rule #8: plan overrides require a human action and must be logged. This endpoint IS
    # that human action; created_by="therapist" plus created_at is the log entry.
    current = _current_plan(db, child_id)
    next_version = current.version + 1 if current else 1
    if current is not None:
        current.status = "superseded"

    new_plan = Plan(
        child_id=child_id,
        version=next_version,
        status="active",
        rationale=override.rationale,
        created_by="therapist",
    )
    db.add(new_plan)
    db.flush()

    for module in override.modules:
        db.add(PlanModule(plan_id=new_plan.id, module=module.module, weight=module.weight))

    db.commit()
    db.refresh(new_plan)
    return _serialize_plan(db, new_plan)
