from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import CursorResult, update
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ActivityRun, ChildSession
from app.schemas.activity_runs import ActivityRunCreateIn, ActivityRunOut, ActivityRunUpdateIn
from app.week1.gate import try_complete_day

router = APIRouter(tags=["activity-runs"])


@router.post("/activity-runs", response_model=ActivityRunOut, status_code=201)
def create_activity_run(payload: ActivityRunCreateIn, db: Session = Depends(get_db)) -> ActivityRun:
    # Checked up front for a clean 404 instead of letting the FK constraint surface as a
    # raw 500 from a bad/expired session_id.
    if db.get(ChildSession, payload.session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")

    run = ActivityRun(
        session_id=payload.session_id,
        activity=payload.activity,
        activity_version=payload.activity_version,
        day_index=payload.day_index,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def _advance_week1_gate(db: Session, run: ActivityRun) -> None:
    # Only week-1 runs carry a day_index; later program activities don't participate in
    # the gate. Idempotent, so it's safe to call on every terminal status, not just the
    # one that happens to finish the day.
    if run.day_index is None:
        return
    session = db.get(ChildSession, run.session_id)
    if session is not None:
        try_complete_day(db, session.child_id, run.day_index)


@router.patch("/activity-runs/{run_id}", response_model=ActivityRunOut)
def update_activity_run(
    run_id: UUID, payload: ActivityRunUpdateIn, db: Session = Depends(get_db)
) -> ActivityRun:
    run = db.get(ActivityRun, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Activity run not found")

    if run.status == payload.status:
        # Same terminal status as already recorded: a retried PATCH from an offline
        # client, not a new event. No-op rather than pushing ended_at forward again.
        _advance_week1_gate(db, run)
        return run
    if run.status != "started":
        raise HTTPException(
            status_code=409,
            detail=f"Activity run is already '{run.status}', cannot set to '{payload.status}'",
        )

    # Conditional UPDATE (not run.status = ...; db.commit()) so the WHERE re-checks
    # status="started" atomically at the DB. Closes the race between the read above and
    # this write: if a concurrent request already transitioned this run, rowcount is 0
    # here instead of silently overwriting its status.
    result = cast(
        CursorResult,
        db.execute(
            update(ActivityRun)
            .where(ActivityRun.id == run_id, ActivityRun.status == "started")
            .values(status=payload.status, ended_at=datetime.now(UTC))
        ),
    )
    db.commit()
    db.refresh(run)

    if result.rowcount == 0:
        if run.status == payload.status:
            _advance_week1_gate(db, run)
            return run
        raise HTTPException(
            status_code=409,
            detail=f"Activity run is already '{run.status}', cannot set to '{payload.status}'",
        )
    _advance_week1_gate(db, run)
    return run
