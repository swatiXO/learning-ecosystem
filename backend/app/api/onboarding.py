from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Child, Consent, Guardian, School
from app.onboarding import options
from app.onboarding.age import age_band
from app.schemas.onboarding import OnboardingIn, OnboardingOut, OptionsOut, SchoolOut

router = APIRouter(tags=["onboarding"])

# Terms version accepted by ConsentIn.terms. Bump this if the terms text changes.
CONSENT_VERSION = "1.0"


@router.get("/onboarding/options", response_model=OptionsOut)
def get_options(q: str | None = None, db: Session = Depends(get_db)) -> OptionsOut:
    stmt = select(School)
    if q:
        stmt = stmt.where(School.name.ilike(f"%{q}%"))
    schools = db.scalars(stmt.order_by(School.name)).all()
    return OptionsOut(
        areas=list(options.AREAS),
        relationships=list(options.RELATIONSHIPS),
        grades=list(options.GRADES),
        languages=list(options.LANGUAGES),
        genders=list(options.GENDERS),
        avatars=list(options.AVATARS),
        schools=[SchoolOut.model_validate(s) for s in schools],
    )


@router.post("/onboarding", response_model=OnboardingOut)
def onboard(payload: OnboardingIn, db: Session = Depends(get_db)) -> OnboardingOut:
    # Guardian + child + consent in one transaction: all or nothing.
    try:
        # OnboardingIn.phone_is_valid already normalised guardian_phone.
        phone = payload.guardian_phone

        # A second sibling onboards with the same phone and reuses the guardian row
        # instead of failing on the phone-unique constraint. Existing name/relationship
        # are kept as-is (not overwritten by whatever this onboarding call typed in).
        # TODO: there is no OTP/phone verification on this endpoint yet, so anyone who
        # knows a guardian's phone number can currently attach a child to their account.
        # Add phone verification before this goes to production.
        guardian = db.scalar(select(Guardian).where(Guardian.phone == phone))
        if guardian is None:
            guardian = Guardian(
                name=payload.guardian_name,
                relationship=payload.guardian_relationship,
                phone=phone,
                locale=payload.locale,
            )
            db.add(guardian)
            db.flush()

        school_id = payload.school_id
        if school_id is not None:
            if db.get(School, school_id) is None:
                raise HTTPException(status_code=422, detail="school_id not found")
        elif payload.schooling == "school":
            # OnboardingIn already guarantees school_name is set when school_id isn't.
            school = School(name=payload.school_name, area=payload.area)
            db.add(school)
            db.flush()
            school_id = school.id

        child = Child(
            guardian_id=guardian.id,
            name=payload.child_name,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            area=payload.area,
            schooling=payload.schooling,
            school_id=school_id,
            grade=payload.grade,
            home_languages=payload.home_languages,
            avatar=payload.avatar,
        )
        db.add(child)
        db.flush()

        db.add(
            Consent(
                child_id=child.id,
                guardian_id=guardian.id,
                version=CONSENT_VERSION,
                audio=payload.consent.audio,
                video=payload.consent.video,
                teacher_share=payload.consent.teacher_share,
            )
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    return OnboardingOut(
        guardian_id=guardian.id,
        child_id=child.id,
        age_band=age_band(payload.date_of_birth, datetime.now(UTC).date()),
    )
