import uuid
from datetime import UTC, datetime

from app.db import SessionLocal
from app.models import SignalEvent


def test_signal_event_round_trip() -> None:
    db = SessionLocal()
    try:
        event = SignalEvent(
            event_id=uuid.uuid4(),
            child_id=uuid.uuid4(),
            session_id=uuid.uuid4(),
            activity_run_id=uuid.uuid4(),
            activity="stars_not_clouds",
            activity_version="1.0.0",
            event_type="tap",
            ts_client=datetime.now(UTC),
            payload={"target": "cloud", "correct": False, "reaction_ms": 412},
        )
        db.add(event)
        db.commit()

        fetched = db.get(SignalEvent, event.event_id)
        assert fetched is not None
        assert fetched.activity == "stars_not_clouds"
        assert fetched.payload["reaction_ms"] == 412
        assert fetched.ts_server is not None

        db.delete(fetched)
        db.commit()
    finally:
        db.close()
