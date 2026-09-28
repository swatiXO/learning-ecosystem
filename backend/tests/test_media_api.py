import uuid
from datetime import UTC, date, datetime

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models import ActivityRun, Child, ChildSession, Consent, Guardian, MediaObject

client = TestClient(app)


def _make_child(db) -> Child:
    guardian = Guardian(
        name="Test Guardian", relationship="mother", phone=f"+92300{uuid.uuid4().int % 10**7:07d}"
    )
    db.add(guardian)
    db.flush()
    child = Child(
        guardian_id=guardian.id,
        name="Test Child",
        date_of_birth=date(2020, 1, 1),
        area="karachi",
        schooling="home_school",
        home_languages=["urdu"],
    )
    db.add(child)
    db.flush()
    return child


def _make_activity_run(db, child_id: uuid.UUID) -> ActivityRun:
    session = ChildSession(child_id=child_id)
    db.add(session)
    db.flush()
    run = ActivityRun(session_id=session.id, activity="speak_this_line", activity_version="1.0.0")
    db.add(run)
    db.flush()
    return run


def _make_consent(db, child: Child, audio: bool, video: bool) -> Consent:
    consent = Consent(
        child_id=child.id,
        guardian_id=child.guardian_id,
        version="v1",
        audio=audio,
        video=video,
    )
    db.add(consent)
    db.flush()
    return consent


def _cleanup(child_id: uuid.UUID) -> None:
    db = SessionLocal()
    try:
        db.query(MediaObject).filter_by(child_id=child_id).delete()
        db.query(Consent).filter_by(child_id=child_id).delete()
        # Deleting the session cascades to its activity_runs (FK ondelete=CASCADE, #11).
        db.query(ChildSession).filter_by(child_id=child_id).delete()
        db.commit()
        child = db.get(Child, child_id)
        if child is not None:
            guardian_id = child.guardian_id
            db.delete(child)
            db.commit()
            guardian = db.get(Guardian, guardian_id)
            if guardian is not None:
                db.delete(guardian)
                db.commit()
    finally:
        db.close()


def test_upload_url_requires_existing_child() -> None:
    response = client.post(
        "/media/upload-url",
        json={
            "child_id": str(uuid.uuid4()),
            "activity_run_id": str(uuid.uuid4()),
            "kind": "audio",
        },
    )
    assert response.status_code == 404


def test_upload_url_requires_activity_run_belonging_to_this_child() -> None:
    db = SessionLocal()
    child = _make_child(db)
    other_child = _make_child(db)
    db.commit()
    child_id, other_child_id = child.id, other_child.id
    run = _make_activity_run(db, other_child_id)
    db.commit()
    run_id = run.id
    db.close()

    try:
        # run_id genuinely exists, but under a different child - must not be usable to
        # attach media to child_id's record.
        response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "audio"},
        )
        assert response.status_code == 404
    finally:
        _cleanup(child_id)
        _cleanup(other_child_id)


def test_upload_url_requires_consent() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    child_id = child.id
    run = _make_activity_run(db, child_id)
    db.commit()
    run_id = run.id
    db.close()

    try:
        response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "audio"},
        )
        assert response.status_code == 403
    finally:
        _cleanup(child_id)


def test_upload_url_checks_the_kind_specific_consent_flag() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    run = _make_activity_run(db, child.id)
    _make_consent(db, child, audio=True, video=False)
    db.commit()
    child_id, run_id = child.id, run.id
    db.close()

    try:
        video_response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "video"},
        )
        assert video_response.status_code == 403

        audio_response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "audio"},
        )
        assert audio_response.status_code == 201
    finally:
        _cleanup(child_id)


def test_upload_url_succeeds_and_persists_a_media_object() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    run = _make_activity_run(db, child.id)
    consent = _make_consent(db, child, audio=True, video=True)
    db.commit()
    child_id, run_id, consent_id = child.id, run.id, consent.id
    db.close()

    try:
        response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "video"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["storage_key"].startswith("video/")
        assert body["media_object_id"] == body["storage_key"].split("/", 1)[1]
        assert "upload_url" in body and body["upload_url"].startswith("http")

        db = SessionLocal()
        try:
            media = db.get(MediaObject, uuid.UUID(body["media_object_id"]))
            assert media is not None
            assert media.child_id == child_id
            assert media.activity_run_id == run_id
            assert media.consent_id == consent_id
            assert media.kind == "video"
        finally:
            db.close()
    finally:
        _cleanup(child_id)


def test_upload_url_ignores_a_revoked_consent() -> None:
    db = SessionLocal()
    child = _make_child(db)
    db.commit()
    run = _make_activity_run(db, child.id)
    consent = _make_consent(db, child, audio=True, video=True)
    db.commit()
    consent.revoked_at = datetime.now(UTC)
    db.commit()
    child_id, run_id = child.id, run.id
    db.close()

    try:
        response = client.post(
            "/media/upload-url",
            json={"child_id": str(child_id), "activity_run_id": str(run_id), "kind": "audio"},
        )
        assert response.status_code == 403
    finally:
        _cleanup(child_id)
