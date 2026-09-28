import uuid
from datetime import UTC, datetime
from typing import Any

from app.models import SignalEvent


def make_event(
    child_id: uuid.UUID,
    activity: str,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> SignalEvent:
    return SignalEvent(
        event_id=uuid.uuid4(),
        child_id=child_id,
        session_id=uuid.uuid4(),
        activity_run_id=uuid.uuid4(),
        activity=activity,
        activity_version="1.0.0",
        event_type=event_type,
        ts_client=datetime.now(UTC),
        payload=payload or {},
    )
