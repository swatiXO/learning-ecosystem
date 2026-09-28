from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.plan_engine.catalog import activities_for_modules
from app.plan_engine.service import current_plan, modules_for_plan
from app.schemas.today import TodayOut
from app.week1.gate import current_day_index
from app.week1.schedule import activities_for_day

router = APIRouter(tags=["today"])


@router.get("/children/{child_id}/today", response_model=TodayOut)
def get_today(child_id: UUID, db: Session = Depends(get_db)) -> TodayOut:
    day = current_day_index(db, child_id)
    if day is not None:
        return TodayOut(
            child_id=child_id,
            phase="week1",
            day_index=day,
            activities=list(activities_for_day(day)),
        )

    plan = current_plan(db, child_id)
    if plan is None:
        # Week 1 is complete but nothing has generated a plan yet — should be rare now
        # that activity-runs.py triggers scoring+replan the moment week 1 finishes
        # (issue #39); this branch mainly covers a child whose data predates that fix.
        raise HTTPException(
            status_code=404,
            detail="Week 1 is complete but no active plan exists yet for this child",
        )

    return TodayOut(
        child_id=child_id,
        phase="plan",
        day_index=None,
        activities=activities_for_modules(modules_for_plan(db, plan)),
        plan_id=plan.id,
    )
