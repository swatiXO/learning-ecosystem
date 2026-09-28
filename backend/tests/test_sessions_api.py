import uuid

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models import ChildSession

client = TestClient(app)


def _delete_session(session_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        session = db.get(ChildSession, session_id)
        if session is not None:
            db.delete(session)
            db.commit()
    finally:
        db.close()


def test_create_session_starts_open_with_no_end_time() -> None:
    child_id = uuid.uuid4()
    response = client.post(
        "/sessions",
        json={"child_id": str(child_id), "device_info": {"os": "android"}, "mood_before": "calm"},
    )
    try:
        assert response.status_code == 201
        body = response.json()
        assert body["child_id"] == str(child_id)
        assert body["device_info"] == {"os": "android"}
        assert body["mood_before"] == "calm"
        assert body["mood_after"] is None
        assert body["ended_at"] is None
        assert body["started_at"] is not None
    finally:
        _delete_session(uuid.UUID(response.json()["id"]))


def test_create_session_defaults_device_info_to_empty_dict() -> None:
    response = client.post("/sessions", json={"child_id": str(uuid.uuid4())})
    try:
        assert response.status_code == 201
        assert response.json()["device_info"] == {}
    finally:
        _delete_session(uuid.UUID(response.json()["id"]))


def test_update_session_sets_ended_at_and_mood_after() -> None:
    created = client.post("/sessions", json={"child_id": str(uuid.uuid4())})
    session_id = created.json()["id"]
    try:
        response = client.patch(f"/sessions/{session_id}", json={"mood_after": "happy"})
        assert response.status_code == 200
        body = response.json()
        assert body["ended_at"] is not None
        assert body["mood_after"] == "happy"
    finally:
        _delete_session(uuid.UUID(session_id))


def test_update_session_is_idempotent_about_ended_at() -> None:
    created = client.post("/sessions", json={"child_id": str(uuid.uuid4())})
    session_id = created.json()["id"]
    try:
        first = client.patch(f"/sessions/{session_id}", json={})
        first_ended_at = first.json()["ended_at"]
        assert first_ended_at is not None

        # A retried PATCH must not push ended_at forward, but should still apply a new
        # mood_after — mood is metadata, not part of the end-session state transition.
        second = client.patch(f"/sessions/{session_id}", json={"mood_after": "sleepy"})
        assert second.json()["ended_at"] == first_ended_at
        assert second.json()["mood_after"] == "sleepy"
    finally:
        _delete_session(uuid.UUID(session_id))


def test_update_session_not_found_returns_404() -> None:
    response = client.patch(f"/sessions/{uuid.uuid4()}", json={"mood_after": "happy"})
    assert response.status_code == 404
