from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.plan_engine.service import current_plan
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
        # Week 1 is done, but nothing recomputes scores or generates a plan automatically
        # yet (PROJECT.md's Track B build log already flags that wiring gap). Surfacing
        # it plainly here rather than a 500 or an empty-but-200 response that looks fine.
        raise HTTPException(
            status_code=404,
            detail="Week 1 is complete but no active plan exists yet for this child",
        )

    return TodayOut(
        child_id=child_id,
        phase="plan",
        day_index=None,
        # No module -> activity catalog exists yet (PRD FR-18's "each module a set of
        # tagged activities" isn't built by any track) - a real content-design gap, not
        # something to invent here. See PROJECT.md build log.
        activities=[],
        plan_id=plan.id,
    )
