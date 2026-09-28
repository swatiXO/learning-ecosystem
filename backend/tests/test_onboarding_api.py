import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.db import SessionLocal
from app.main import app
from app.models import Child, Consent, Guardian, Plan, School, SkillScore
from app.onboarding.age import age_band

client = TestClient(app)


def _unique_phone() -> str:
    return f"+9230{uuid.uuid4().int % 10**8:08d}"


def _payload(phone: str, **overrides) -> dict:
    data = {
        "guardian_name": "Test Guardian",
        "guardian_relationship": "mother",
        "guardian_phone": phone,
        "locale": "en",
        "child_name": "Test Child",
        "date_of_birth": "2020-01-01",
        "area": "karachi",
        "schooling": "home_school",
        "home_languages": ["urdu"],
        "consent": {"terms": True, "audio": False, "video": False},
    }
    data.update(overrides)
    return data


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


def test_onboarding_happy_path_home_school() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone))
    assert response.status_code == 200
    body = response.json()
    try:
        assert uuid.UUID(body["guardian_id"])
        assert uuid.UUID(body["child_id"])
        expected_band = age_band(date(2020, 1, 1), datetime.now(UTC).date())
        assert body["age_band"] == expected_band
    finally:
        _cleanup(child_ids=[body["child_id"]], guardian_ids=[body["guardian_id"]])


def test_onboarding_school_with_school_name_creates_school() -> None:
    phone = _unique_phone()
    school_name = f"Test School {uuid.uuid4().hex[:8]}"
    response = client.post(
        "/onboarding",
        json=_payload(phone, schooling="school", school_name=school_name, area="lahore"),
    )
    assert response.status_code == 200
    body = response.json()
    db = SessionLocal()
    try:
        child = db.get(Child, uuid.UUID(body["child_id"]))
        assert child is not None
        assert child.school_id is not None
        school = db.get(School, child.school_id)
        assert school is not None
        assert school.name == school_name
        assert school.area == "lahore"
    finally:
        db.close()
        _cleanup(
            child_ids=[body["child_id"]],
            guardian_ids=[body["guardian_id"]],
            school_ids=[str(child.school_id)],
        )


def test_onboarding_school_with_existing_school_id() -> None:
    db = SessionLocal()
    school = School(name="Existing Test School", area="karachi")
    db.add(school)
    db.commit()
    school_id = school.id
    db.close()

    phone = _unique_phone()
    response = client.post(
        "/onboarding",
        json=_payload(phone, schooling="school", school_id=str(school_id)),
    )
    assert response.status_code == 200
    body = response.json()
    try:
        db = SessionLocal()
        child = db.get(Child, uuid.UUID(body["child_id"]))
        assert child.school_id == school_id
        db.close()
    finally:
        _cleanup(
            child_ids=[body["child_id"]],
            guardian_ids=[body["guardian_id"]],
            school_ids=[school_id],
        )


def test_onboarding_school_missing_both_fields_is_422() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone, schooling="school"))
    assert response.status_code == 422


def test_onboarding_invalid_relationship_is_422() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone, guardian_relationship="uncle"))
    assert response.status_code == 422


def test_onboarding_invalid_area_is_422() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone, area="atlantis"))
    assert response.status_code == 422


def test_onboarding_future_dob_is_422() -> None:
    phone = _unique_phone()
    future = (datetime.now(UTC).date() + timedelta(days=1)).isoformat()
    response = client.post("/onboarding", json=_payload(phone, date_of_birth=future))
    assert response.status_code == 422


def test_onboarding_too_young_dob_is_422() -> None:
    phone = _unique_phone()
    too_young = datetime.now(UTC).date().replace(year=datetime.now(UTC).year - 1).isoformat()
    response = client.post("/onboarding", json=_payload(phone, date_of_birth=too_young))
    assert response.status_code == 422


def test_onboarding_too_old_dob_is_422() -> None:
    phone = _unique_phone()
    too_old = datetime.now(UTC).date().replace(year=datetime.now(UTC).year - 25).isoformat()
    response = client.post("/onboarding", json=_payload(phone, date_of_birth=too_old))
    assert response.status_code == 422


def test_onboarding_empty_home_languages_is_422() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone, home_languages=[]))
    assert response.status_code == 422


def test_onboarding_consent_terms_false_is_422() -> None:
    phone = _unique_phone()
    response = client.post(
        "/onboarding",
        json=_payload(phone, consent={"terms": False, "audio": False, "video": False}),
    )
    assert response.status_code == 422


def test_onboarding_sibling_reuses_guardian() -> None:
    phone = _unique_phone()
    first = client.post(
        "/onboarding", json=_payload(phone, guardian_name="Original Name", child_name="Sibling One")
    )
    second = client.post(
        "/onboarding",
        json=_payload(phone, guardian_name="Different Name", child_name="Sibling Two"),
    )
    assert first.status_code == 200
    assert second.status_code == 200
    body1, body2 = first.json(), second.json()
    try:
        assert body1["guardian_id"] == body2["guardian_id"]
        assert body1["child_id"] != body2["child_id"]

        db = SessionLocal()
        guardian = db.get(Guardian, uuid.UUID(body1["guardian_id"]))
        assert guardian.name == "Original Name"

        children = db.query(Child).filter_by(guardian_id=guardian.id).all()
        assert len(children) == 2

        consents = db.query(Consent).filter(Consent.child_id.in_([c.id for c in children])).all()
        assert len(consents) == 2
        db.close()
    finally:
        _cleanup(
            child_ids=[body1["child_id"], body2["child_id"]],
            guardian_ids=[body1["guardian_id"]],
        )


def test_onboarding_options_lists_schools_and_option_values() -> None:
    db = SessionLocal()
    school = School(name=f"Searchable School {uuid.uuid4().hex[:8]}", area="karachi")
    db.add(school)
    db.commit()
    school_id, school_name = school.id, school.name
    db.close()

    try:
        response = client.get("/onboarding/options", params={"q": school_name[:15]})
        assert response.status_code == 200
        body = response.json()
        assert "karachi" in body["areas"]
        assert "mother" in body["relationships"]
        assert "urdu" in body["languages"]
        assert any(s["id"] == str(school_id) for s in body["schools"])
    finally:
        db = SessionLocal()
        db.query(School).filter_by(id=school_id).delete()
        db.commit()
        db.close()


def test_onboarding_writes_no_skill_scores_or_plans() -> None:
    phone = _unique_phone()
    response = client.post("/onboarding", json=_payload(phone))
    assert response.status_code == 200
    body = response.json()
    child_id = uuid.UUID(body["child_id"])
    try:
        db = SessionLocal()
        assert db.query(SkillScore).filter_by(child_id=child_id).count() == 0
        assert db.query(Plan).filter_by(child_id=child_id).count() == 0
        db.close()
    finally:
        _cleanup(child_ids=[body["child_id"]], guardian_ids=[body["guardian_id"]])
