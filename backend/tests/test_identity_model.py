import uuid
from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from app.db import SessionLocal
from app.models import Child, Consent, Guardian, School


def _make_guardian(db, phone: str = "+923001234567") -> Guardian:
    guardian = Guardian(name="Test Guardian", relationship="mother", phone=phone)
    db.add(guardian)
    db.flush()
    return guardian


def test_child_rejects_school_without_school_id() -> None:
    db = SessionLocal()
    try:
        guardian = _make_guardian(db)
        db.add(
            Child(
                guardian_id=guardian.id,
                name="Test Child",
                date_of_birth=date(2020, 1, 1),
                area="karachi",
                schooling="school",
                school_id=None,
                home_languages=["urdu"],
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.close()


def test_child_rejects_invalid_schooling_value() -> None:
    db = SessionLocal()
    try:
        guardian = _make_guardian(db)
        db.add(
            Child(
                guardian_id=guardian.id,
                name="Test Child",
                date_of_birth=date(2020, 1, 1),
                area="karachi",
                schooling="bootcamp",
                home_languages=["urdu"],
            )
        )
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.close()


def test_child_accepts_school_with_school_id() -> None:
    db = SessionLocal()
    try:
        guardian = _make_guardian(db)
        school = School(name="Test School", area="karachi")
        db.add(school)
        db.flush()

        child = Child(
            guardian_id=guardian.id,
            name="Test Child",
            date_of_birth=date(2020, 1, 1),
            area="karachi",
            schooling="school",
            school_id=school.id,
            home_languages=["urdu", "english"],
        )
        db.add(child)
        db.commit()

        fetched = db.get(Child, child.id)
        assert fetched is not None
        assert fetched.home_languages == ["urdu", "english"]
    finally:
        db.rollback()
        db.query(Child).filter_by(guardian_id=guardian.id).delete()
        db.query(School).filter_by(id=school.id).delete()
        db.query(Guardian).filter_by(id=guardian.id).delete()
        db.commit()
        db.close()


def test_child_accepts_home_school_without_school_id() -> None:
    db = SessionLocal()
    try:
        guardian = _make_guardian(db)
        child = Child(
            guardian_id=guardian.id,
            name="Test Child",
            date_of_birth=date(2020, 1, 1),
            area="karachi",
            schooling="home_school",
            home_languages=["urdu"],
        )
        db.add(child)
        db.commit()
        assert db.get(Child, child.id) is not None
    finally:
        db.rollback()
        db.query(Child).filter_by(guardian_id=guardian.id).delete()
        db.query(Guardian).filter_by(id=guardian.id).delete()
        db.commit()
        db.close()


def test_guardian_phone_is_unique() -> None:
    db = SessionLocal()
    phone = f"+9230012{uuid.uuid4().int % 100000:05d}"
    try:
        db.add(Guardian(name="First", relationship="mother", phone=phone))
        db.commit()

        db.add(Guardian(name="Second", relationship="father", phone=phone))
        with pytest.raises(IntegrityError):
            db.commit()
    finally:
        db.rollback()
        db.query(Guardian).filter_by(phone=phone).delete()
        db.commit()
        db.close()


def test_deleting_child_cascades_to_consents() -> None:
    db = SessionLocal()
    try:
        guardian = _make_guardian(db)
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

        consent = Consent(
            child_id=child.id,
            guardian_id=guardian.id,
            version="1.0",
            audio=False,
            video=False,
        )
        db.add(consent)
        db.commit()
        consent_id = consent.id

        db.delete(db.get(Child, child.id))
        db.commit()
        db.expire_all()

        assert db.get(Consent, consent_id) is None
    finally:
        db.rollback()
        db.query(Guardian).filter_by(id=guardian.id).delete()
        db.commit()
        db.close()
