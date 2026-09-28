"""Pure onboarding validation and normalisation. No DB or FastAPI imports — these are
called from Pydantic validators in app/schemas/onboarding.py and app/schemas/children.py,
and unit-tested directly."""

import re
from datetime import date
from uuid import UUID

from app.onboarding.age import age_in_years

MIN_PLAUSIBLE_AGE = 3
MAX_PLAUSIBLE_AGE = 18

# +92 followed by a 10-digit Pakistani mobile number (starts with 3). Excludes
# landlines, which don't start with 3.
PAKISTANI_MOBILE_PATTERN = re.compile(r"^\+923\d{9}$")


def normalize_phone(raw: str) -> str:
    """Collapse Pakistani mobile phone formats to one E.164-ish form, so
    "0300-1234567", "03001234567" and "+923001234567" all become the same guardian
    lookup key. Raises ValueError if the result isn't a Pakistani mobile number."""
    digits = "".join(ch for ch in raw if ch.isdigit())
    if digits.startswith("92"):
        national = digits[2:]
    elif digits.startswith("0"):
        national = digits[1:]
    else:
        national = digits
    normalized = "+92" + national
    if not PAKISTANI_MOBILE_PATTERN.match(normalized):
        raise ValueError(f"'{raw}' is not a valid Pakistani mobile number")
    return normalized


def validate_date_of_birth(dob: date, today: date) -> None:
    if dob > today:
        raise ValueError("date of birth cannot be in the future")
    age = age_in_years(dob, today)
    if age < MIN_PLAUSIBLE_AGE or age > MAX_PLAUSIBLE_AGE:
        raise ValueError(
            f"date of birth implies age {age}, which is outside the plausible range "
            f"{MIN_PLAUSIBLE_AGE}-{MAX_PLAUSIBLE_AGE}"
        )


def validate_schooling(schooling: str, school_id: UUID | None, school_name: str | None) -> None:
    if schooling == "school" and not school_id and not school_name:
        raise ValueError("school_id or school_name is required when schooling is 'school'")


def validate_home_languages(languages: list[str]) -> None:
    if not languages:
        raise ValueError("at least one home language is required")


def validate_consent_terms(terms: bool) -> None:
    if not terms:
        raise ValueError("consent terms must be accepted")
