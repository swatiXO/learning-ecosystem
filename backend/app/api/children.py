from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Child, Consent, School
from app.onboarding.validation import (
    validate_date_of_birth,
    validate_home_languages,
    validate_schooling,
)
from app.schemas.children import ChildOut, ChildUpdateIn, ConsentOut, ConsentUpdateIn

router = APIRouter(tags=["children"])

# These columns are NOT NULL on Child (PROJECT.md §6); a PATCH may omit them but must
# not null them out. gender/grade/avatar/school_id are nullable and may be set to null.
REQUIRED_CHILD_FIELDS = ("name", "date_of_birth", "area", "schooling", "home_languages")


def _get_child_or_404(db: Session, child_id: UUID) -> Child:
    child = db.get(Child, child_id)
    if child is None:
        raise HTTPException(status_code=404, detail="child not found")
    return child


def _validation_error(errors: list[tuple[str, str, Any]]) -> RequestValidationError:
    """Build a 422 body shaped like Pydantic's own: {"detail": [{"type", "loc", "msg",
    "input"}, ...]}, so PATCH errors raised from router code (as opposed to a Pydantic
    validator) still look the same to a client."""
    return RequestValidationError(
        [
            {
                "type": "value_error",
                "loc": ["body", field],
                "msg": f"Value error, {msg}",
                "input": value,
            }
            for field, msg, value in errors
        ]
    )


@router.patch("/children/{child_id}", response_model=ChildOut)
def update_child(child_id: UUID, payload: ChildUpdateIn, db: Session = Depends(get_db)) -> ChildOut:
    child = _get_child_or_404(db, child_id)
    updates = payload.model_dump(exclude_unset=True)

    null_required = [f for f in REQUIRED_CHILD_FIELDS if f in updates and updates[f] is None]
    if null_required:
        raise _validation_error(
            [(f, "this field is required and cannot be null", None) for f in null_required]
        )

    final_dob = updates.get("date_of_birth", child.date_of_birth)
    final_schooling = updates.get("schooling", child.schooling)
    final_area = updates.get("area", child.area)
    explicit_school_id = updates.get("school_id")
    school_name = updates.get("school_name")
    effective_school_id = explicit_school_id if "school_id" in updates else child.school_id

    # Only check the age range when the DOB itself is being changed: a child who has
    # aged past 12 since onboarding must still be able to edit their other fields.
    if "date_of_birth" in updates:
        try:
            validate_date_of_birth(final_dob, datetime.now(UTC).date())
        except ValueError as exc:
            raise _validation_error([("date_of_birth", str(exc), final_dob)]) from exc

    try:
        validate_schooling(final_schooling, effective_school_id, school_name)
    except ValueError as exc:
        raise _validation_error([("schooling", str(exc), final_schooling)]) from exc

    if "home_languages" in updates:
        try:
            validate_home_languages(updates["home_languages"])
        except ValueError as exc:
            raise _validation_error(
                [("home_languages", str(exc), updates["home_languages"])]
            ) from exc

    # Rule: switching to home_school always clears any existing/incoming school link.
    if final_schooling == "home_school":
        new_school_id = None
    elif explicit_school_id is not None:
        if db.get(School, explicit_school_id) is None:
            raise _validation_error([("school_id", "school_id not found", explicit_school_id)])
        new_school_id = explicit_school_id
    elif school_name is not None:
        school = School(name=school_name, area=final_area)
        db.add(school)
        db.flush()
        new_school_id = school.id
    else:
        new_school_id = child.school_id

    for field, value in updates.items():
        if field in ("school_id", "school_name"):
            continue
        setattr(child, field, value)
    child.school_id = new_school_id

    db.commit()
    db.refresh(child)
    return ChildOut.model_validate(child)


@router.post("/children/{child_id}/consent", response_model=ConsentOut)
def add_consent(
    child_id: UUID, payload: ConsentUpdateIn, db: Session = Depends(get_db)
) -> ConsentOut:
    child = _get_child_or_404(db, child_id)

    previous = db.scalar(
        select(Consent)
        .where(Consent.child_id == child_id, Consent.revoked_at.is_(None))
        .order_by(Consent.granted_at.desc())
    )
    if previous is not None:
        previous.revoked_at = datetime.now(UTC)

    consent = Consent(
        child_id=child.id,
        guardian_id=child.guardian_id,
        version=payload.version,
        audio=payload.audio,
        video=payload.video,
        teacher_share=payload.teacher_share,
    )
    db.add(consent)
    db.commit()
    db.refresh(consent)
    return ConsentOut.model_validate(consent)
