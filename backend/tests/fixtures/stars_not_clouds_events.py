import uuid
from datetime import UTC, datetime

from app.models import SignalEvent


def make_tap(child_id: uuid.UUID, target: str, reaction_ms: int | None = None) -> SignalEvent:
    correct = target == "star"
    return SignalEvent(
        event_id=uuid.uuid4(),
        child_id=child_id,
        session_id=uuid.uuid4(),
        activity_run_id=uuid.uuid4(),
        activity="stars_not_clouds",
        activity_version="1.0.0",
        event_type="tap",
        ts_client=datetime.now(UTC),
        payload={"target": target, "correct": correct, "reaction_ms": reaction_ms},
    )
