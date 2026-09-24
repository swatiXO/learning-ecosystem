from fastapi import APIRouter, Depends
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import SignalEvent
from app.schemas.events import EventBatchIn, EventBatchResult

router = APIRouter(tags=["events"])


@router.post("/events/batch", response_model=EventBatchResult)
def ingest_events(batch: EventBatchIn, db: Session = Depends(get_db)) -> EventBatchResult:
    if not batch.events:
        return EventBatchResult(accepted=0, duplicates=0)

    rows = [
        {
            "event_id": event.event_id,
            "child_id": event.child_id,
            "session_id": event.session_id,
            "activity_run_id": event.activity_run_id,
            "activity": event.activity,
            "activity_version": event.activity_version,
            "event_type": event.event_type,
            "ts_client": event.ts_client,
            "payload": event.payload,
        }
        for event in batch.events
    ]

    stmt = (
        insert(SignalEvent)
        .values(rows)
        .on_conflict_do_nothing(index_elements=["event_id"])
        .returning(SignalEvent.event_id)
    )
    accepted = len(db.execute(stmt).fetchall())
    db.commit()

    return EventBatchResult(accepted=accepted, duplicates=len(rows) - accepted)
