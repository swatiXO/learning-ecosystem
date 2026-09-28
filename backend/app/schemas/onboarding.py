from datetime import UTC, date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, field_validator, model_validator

from app.onboarding import options
from app.onboarding.validation import (
    normalize_phone,
    validate_consent_terms,
    validate_date_of_birth,
    validate_home_languages,
    validate_schooling,
)

Schooling = Literal["school", "home_school"]


class ConsentIn(BaseModel):
    terms: bool
    audio: bool
    video: bool
    teacher_share: bool = False

    @model_validator(mode="after")
    def check_terms(self) -> "ConsentIn":
        validate_consent_terms(self.terms)
        return self


class OnboardingIn(BaseModel):
    guardian_name: str
    guardian_relationship: str
    guardian_phone: str
    locale: str = "en"

    child_name: str
    date_of_birth: date
    area: str
    schooling: Schooling
    school_id: UUID | None = None
    school_name: str | None = None
    grade: str | None = None
    home_languages: list[str]
    gender: str | None = None
    avatar: str | None = None

    consent: ConsentIn

    @field_validator("guardian_phone")
    @classmethod
    def phone_is_valid(cls, value: str) -> str:
        return normalize_phone(value)

    @field_validator("guardian_relationship")
    @classmethod
    def relationship_is_known(cls, value: str) -> str:
        if value not in options.RELATIONSHIPS:
            raise ValueError(f"relationship must be one of {options.RELATIONSHIPS}")
        return value

    @field_validator("area")
    @classmethod
    def area_is_known(cls, value: str) -> str:
        if value not in options.AREAS:
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
    def languages_are_known(cls, value: list[str]) -> list[str]:
        validate_home_languages(value)
        unknown = [v for v in value if v not in options.LANGUAGES]
        if unknown:
            raise ValueError(f"unknown home languages: {unknown}")
        return value

    @model_validator(mode="after")
    def check_dob(self) -> "OnboardingIn":
        validate_date_of_birth(self.date_of_birth, datetime.now(UTC).date())
        return self

    @model_validator(mode="after")
    def check_schooling(self) -> "OnboardingIn":
        validate_schooling(self.schooling, self.school_id, self.school_name)
        return self


class OnboardingOut(BaseModel):
    guardian_id: UUID
    child_id: UUID
    age_band: str


class SchoolOut(BaseModel):
    id: UUID
    name: str
    area: str

    model_config = {"from_attributes": True}


class OptionsOut(BaseModel):
    areas: list[str]
    relationships: list[str]
    grades: list[str]
    languages: list[str]
    genders: list[str]
    avatars: list[str]
    schools: list[SchoolOut]
