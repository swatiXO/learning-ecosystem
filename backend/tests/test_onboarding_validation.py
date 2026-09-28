from datetime import date

import pytest

from app.onboarding.validation import (
    normalize_phone,
    validate_consent_terms,
    validate_date_of_birth,
    validate_home_languages,
    validate_schooling,
)


@pytest.mark.parametrize(
    "raw",
    ["0300-1234567", "03001234567", "+923001234567", "923001234567", "0300 123 4567"],
)
def test_normalize_phone_variants_match(raw: str) -> None:
    assert normalize_phone(raw) == "+923001234567"


def test_validate_date_of_birth_future_rejected() -> None:
    today = date(2026, 1, 1)
    with pytest.raises(ValueError):
        validate_date_of_birth(date(2026, 1, 2), today)


def test_validate_date_of_birth_today_is_allowed_if_plausible() -> None:
    # A newborn is below the plausible range, so DOB "today" should fail on age, not
    # on being in the future.
    today = date(2026, 1, 1)
    with pytest.raises(ValueError):
        validate_date_of_birth(today, today)


def test_validate_date_of_birth_leap_day() -> None:
    validate_date_of_birth(date(2020, 2, 29), date(2026, 3, 1))


def test_validate_date_of_birth_too_young_rejected() -> None:
    today = date(2026, 1, 1)
    with pytest.raises(ValueError):
        validate_date_of_birth(date(2024, 1, 1), today)


def test_validate_date_of_birth_too_old_rejected() -> None:
    today = date(2026, 1, 1)
    with pytest.raises(ValueError):
        validate_date_of_birth(date(2000, 1, 1), today)


def test_validate_date_of_birth_plausible_accepted() -> None:
    validate_date_of_birth(date(2020, 1, 1), date(2026, 1, 1))


def test_validate_schooling_requires_school_id_or_name() -> None:
    with pytest.raises(ValueError):
        validate_schooling("school", None, None)


def test_validate_schooling_accepts_school_id() -> None:
    validate_schooling("school", "some-id", None)


def test_validate_schooling_accepts_school_name() -> None:
    validate_schooling("school", None, "Test School")


def test_validate_schooling_home_school_needs_neither() -> None:
    validate_schooling("home_school", None, None)


def test_validate_home_languages_empty_rejected() -> None:
    with pytest.raises(ValueError):
        validate_home_languages([])


def test_validate_home_languages_accepted() -> None:
    validate_home_languages(["urdu"])


def test_validate_consent_terms_false_rejected() -> None:
    with pytest.raises(ValueError):
        validate_consent_terms(False)


def test_validate_consent_terms_true_accepted() -> None:
    validate_consent_terms(True)
