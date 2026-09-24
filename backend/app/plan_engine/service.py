import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Plan, PlanModule, SkillScore
from app.plan_engine.engine import build_plan
from app.plan_engine.rules import Profile
from app.schemas.plans import PlanModuleOut, PlanOut


def current_plan(db: Session, child_id: uuid.UUID) -> Plan | None:
    return db.scalar(
        select(Plan)
        .where(Plan.child_id == child_id, Plan.status == "active")
        .order_by(Plan.version.desc())
    )


def replace_active_plan(
    db: Session,
    child_id: uuid.UUID,
    modules: dict[str, float],
    rationale: dict[str, Any],
    created_by: str,
) -> Plan:
    existing = current_plan(db, child_id)
    next_version = existing.version + 1 if existing else 1
    if existing is not None:
        existing.status = "superseded"

    new_plan = Plan(
        child_id=child_id,
        version=next_version,
        status="active",
        rationale=rationale,
        created_by=created_by,
    )
    db.add(new_plan)
    db.flush()

    for module, weight in modules.items():
        db.add(PlanModule(plan_id=new_plan.id, module=module, weight=weight))

    db.flush()
    return new_plan


def regenerate_plan(db: Session, child_id: uuid.UUID) -> Plan:
    scores = db.scalars(
        select(SkillScore)
        .where(SkillScore.child_id == child_id)
        .order_by(SkillScore.computed_at.asc())
    ).all()
    profile = Profile.from_scores(list(scores))
    result = build_plan(profile)
    return replace_active_plan(
        db,
        child_id,
        modules=result.modules,
        rationale={"rules_fired": result.rules_fired},
        created_by="engine",
    )


def serialize_plan(db: Session, plan: Plan) -> PlanOut:
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
