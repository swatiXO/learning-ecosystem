from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.onboarding import options
from app.onboarding.validation import validate_home_languages
from app.schemas.onboarding import Schooling


class ChildUpdateIn(BaseModel):
    """Partial update for onboarding answers (PRD FR-4). Only per-field shape/enum
    checks happen here; cross-field rules (schooling vs school_id/school_name, DOB
    plausibility) are re-validated in app/api/children.py against the merged row,
    since a PATCH may touch only one of several related fields."""

    name: str | None = None
    date_of_birth: date | None = None
    area: str | None = None
    schooling: Schooling | None = None
    school_id: UUID | None = None
    school_name: str | None = None
    grade: str | None = None
    home_languages: list[str] | None = None
    gender: str | None = None
    avatar: str | None = None

    @field_validator("area")
    @classmethod
    def area_is_known(cls, value: str | None) -> str | None:
        if value is not None and value not in options.AREAS:
            raise ValueError(f"area must be one of {options.AREAS}")
        return value

    @field_validator("grade")
    @classmethod
    def grade_is_known(cls, value: str | None) -> str | None:
        if value is not None and value not in options.GRADES:
            raise ValueError(f"grade must be one of {options.GRADES}")
        return value

    @field_validator("gender")
    @classmethod
    def gender_is_known(cls, value: str | None) -> str | None:
        if value is not None and value not in options.GENDERS:
            raise ValueError(f"gender must be one of {options.GENDERS}")
        return value

    @field_validator("avatar")
    @classmethod
    def avatar_is_known(cls, value: str | None) -> str | None:
        if value is not None and value not in options.AVATARS:
            raise ValueError(f"avatar must be one of {options.AVATARS}")
        return value

    @field_validator("home_languages")
    @classmethod
    def languages_are_known(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        validate_home_languages(value)
        unknown = [v for v in value if v not in options.LANGUAGES]
        if unknown:
            raise ValueError(f"unknown home languages: {unknown}")
        return value


class ChildOut(BaseModel):
    id: UUID
    guardian_id: UUID
    name: str
    date_of_birth: date
    gender: str | None
    area: str
    schooling: str
    school_id: UUID | None
    grade: str | None
    home_languages: list[str]
    avatar: str | None
    onboarded_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class ConsentUpdateIn(BaseModel):
    version: str
    audio: bool
    video: bool
    teacher_share: bool = False


class ConsentOut(BaseModel):
    id: UUID
    child_id: UUID
    guardian_id: UUID
    version: str
    audio: bool
    video: bool
    teacher_share: bool
    granted_at: datetime
    revoked_at: datetime | None

    model_config = {"from_attributes": True}
