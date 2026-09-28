from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import ChildSession
from app.schemas.sessions import SessionCreateIn, SessionOut, SessionUpdateIn

router = APIRouter(tags=["sessions"])


@router.post("/sessions", response_model=SessionOut, status_code=201)
def create_session(payload: SessionCreateIn, db: Session = Depends(get_db)) -> ChildSession:
    session = ChildSession(
        child_id=payload.child_id,
        device_info=payload.device_info,
        mood_before=payload.mood_before,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@router.patch("/sessions/{session_id}", response_model=SessionOut)
def update_session(
    session_id: UUID, payload: SessionUpdateIn, db: Session = Depends(get_db)
) -> ChildSession:
    session = db.get(ChildSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # First-write-wins: a retried PATCH (offline client, dropped response) must not push
    # ended_at forward on every replay.
    if session.ended_at is None:
        session.ended_at = datetime.now(UTC)
    if payload.mood_after is not None:
        session.mood_after = payload.mood_after

    db.commit()
    db.refresh(session)
    return session
