import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import SignalEvent

client = TestClient(app)


def _make_event(event_id: uuid.UUID) -> dict:
    return {
        "event_id": str(event_id),
        "child_id": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "activity_run_id": str(uuid.uuid4()),
        "activity": "stars_not_clouds",
        "activity_version": "1.0.0",
        "event_type": "tap",
        "ts_client": datetime.now(UTC).isoformat(),
        "payload": {"target": "cloud", "correct": False, "reaction_ms": 412},
    }


def test_events_batch_is_idempotent() -> None:
    event_ids = [uuid.uuid4(), uuid.uuid4()]
    events = [_make_event(eid) for eid in event_ids]

    try:
        first = client.post("/events/batch", json={"events": events})
        assert first.status_code == 200
        assert first.json() == {"accepted": 2, "duplicates": 0}

        second = client.post("/events/batch", json={"events": events})
        assert second.status_code == 200
        assert second.json() == {"accepted": 0, "duplicates": 2}
    finally:
        db = SessionLocal()
        try:
            db.execute(delete(SignalEvent).where(SignalEvent.event_id.in_(event_ids)))
            db.commit()
        finally:
            db.close()


def test_events_batch_empty() -> None:
    response = client.post("/events/batch", json={"events": []})
    assert response.status_code == 200
    assert response.json() == {"accepted": 0, "duplicates": 0}
