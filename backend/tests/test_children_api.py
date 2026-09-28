import uuid

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import Child, Consent, Guardian, School

client = TestClient(app)


def _unique_phone() -> str:
    return f"+9230{uuid.uuid4().int % 10**8:08d}"


def _onboard(**overrides) -> dict:
    payload = {
        "guardian_name": "Test Guardian",
        "guardian_relationship": "mother",
        "guardian_phone": _unique_phone(),
        "locale": "en",
        "child_name": "Test Child",
        "date_of_birth": "2020-01-01",
        "area": "karachi",
        "schooling": "home_school",
        "home_languages": ["urdu"],
        "consent": {"terms": True, "audio": False, "video": False},
    }
    payload.update(overrides)
    response = client.post("/onboarding", json=payload)
    assert response.status_code == 200
    return response.json()


def _cleanup(child_ids=(), guardian_ids=(), school_ids=()) -> None:
    db = SessionLocal()
    try:
        if child_ids:
            db.execute(delete(Consent).where(Consent.child_id.in_(child_ids)))
            db.execute(delete(Child).where(Child.id.in_(child_ids)))
        if school_ids:
            db.execute(delete(School).where(School.id.in_(school_ids)))
        if guardian_ids:
            db.execute(delete(Guardian).where(Guardian.id.in_(guardian_ids)))
        db.commit()
    finally:
        db.close()


def _assert_pydantic_shaped_422(body: dict) -> None:
    assert isinstance(body["detail"], list)
    assert body["detail"], "expected at least one error"
    for error in body["detail"]:
        assert {"type", "loc", "msg", "input"} <= error.keys()


def test_patch_child_updates_a_field() -> None:
    onboarded = _onboard()
    try:
        response = client.patch(f"/children/{onboarded['child_id']}", json={"area": "lahore"})
        assert response.status_code == 200
        assert response.json()["area"] == "lahore"

        db = SessionLocal()
        child = db.get(Child, uuid.UUID(onboarded["child_id"]))
        assert child.area == "lahore"
        db.close()
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_school_name_creates_new_school() -> None:
    onboarded = _onboard()
    school_name = f"Patched School {uuid.uuid4().hex[:8]}"
    try:
        response = client.patch(
            f"/children/{onboarded['child_id']}",
            json={"schooling": "school", "school_name": school_name},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["schooling"] == "school"
        assert body["school_id"] is not None

        db = SessionLocal()
        school = db.get(School, uuid.UUID(body["school_id"]))
        assert school is not None
        assert school.name == school_name
        db.close()
    finally:
        _cleanup(
            child_ids=[onboarded["child_id"]],
            guardian_ids=[onboarded["guardian_id"]],
            school_ids=[body["school_id"]],
        )


def test_patch_child_switch_to_school_without_id_or_name_is_422() -> None:
    onboarded = _onboard()
    try:
        response = client.patch(f"/children/{onboarded['child_id']}", json={"schooling": "school"})
        assert response.status_code == 422
        _assert_pydantic_shaped_422(response.json())
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_empty_home_languages_is_422() -> None:
    onboarded = _onboard()
    try:
        response = client.patch(f"/children/{onboarded['child_id']}", json={"home_languages": []})
        assert response.status_code == 422
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_null_required_field_is_422() -> None:
    onboarded = _onboard()
    try:
        response = client.patch(f"/children/{onboarded['child_id']}", json={"name": None})
        assert response.status_code == 422
        _assert_pydantic_shaped_422(response.json())
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_null_date_of_birth_is_422() -> None:
    onboarded = _onboard()
    try:
        response = client.patch(f"/children/{onboarded['child_id']}", json={"date_of_birth": None})
        assert response.status_code == 422
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_nullable_fields_accept_null() -> None:
    onboarded = _onboard(gender="male", grade=None, avatar="fox")
    try:
        response = client.patch(
            f"/children/{onboarded['child_id']}",
            json={"gender": None, "avatar": None},
        )
        assert response.status_code == 200
        body = response.json()
        assert body["gender"] is None
        assert body["avatar"] is None
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_patch_child_switch_to_home_school_clears_school_id() -> None:
    school_name = f"To Be Left School {uuid.uuid4().hex[:8]}"
    onboarded = _onboard(schooling="school", school_name=school_name)
    school_id = None
    try:
        db = SessionLocal()
        child = db.get(Child, uuid.UUID(onboarded["child_id"]))
        school_id = child.school_id
        assert school_id is not None
        db.close()

        response = client.patch(
            f"/children/{onboarded['child_id']}", json={"schooling": "home_school"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["schooling"] == "home_school"
        assert body["school_id"] is None

        db = SessionLocal()
        refreshed = db.get(Child, uuid.UUID(onboarded["child_id"]))
        assert refreshed.school_id is None
        db.close()
    finally:
        _cleanup(
            child_ids=[onboarded["child_id"]],
            guardian_ids=[onboarded["guardian_id"]],
            school_ids=[str(school_id)] if school_id else [],
        )


def test_patch_unknown_child_is_404() -> None:
    response = client.patch(f"/children/{uuid.uuid4()}", json={"area": "lahore"})
    assert response.status_code == 404


def test_add_consent_creates_history_without_overwriting() -> None:
    onboarded = _onboard()
    try:
        response = client.post(
            f"/children/{onboarded['child_id']}/consent",
            json={"version": "2.0", "audio": True, "video": False, "teacher_share": True},
        )
        assert response.status_code == 200
        new_consent = response.json()
        assert new_consent["revoked_at"] is None
        assert new_consent["version"] == "2.0"

        db = SessionLocal()
        consents = (
            db.query(Consent)
            .filter_by(child_id=uuid.UUID(onboarded["child_id"]))
            .order_by(Consent.granted_at)
            .all()
        )
        assert len(consents) == 2
        assert consents[0].version == "1.0"
        assert consents[0].revoked_at is not None
        assert consents[1].version == "2.0"
        assert consents[1].revoked_at is None
        db.close()
    finally:
        _cleanup(child_ids=[onboarded["child_id"]], guardian_ids=[onboarded["guardian_id"]])


def test_add_consent_unknown_child_is_404() -> None:
    response = client.post(
        f"/children/{uuid.uuid4()}/consent",
        json={"version": "1.0", "audio": False, "video": False},
    )
    assert response.status_code == 404
