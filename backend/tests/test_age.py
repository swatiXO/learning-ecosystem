from datetime import date

from app.onboarding.age import age_band, age_in_years


def test_age_in_years_birthday_today() -> None:
    dob = date(2020, 9, 28)
    today = date(2026, 9, 28)
    assert age_in_years(dob, today) == 6


def test_age_in_years_day_before_birthday() -> None:
    dob = date(2020, 9, 29)
    today = date(2026, 9, 28)
    assert age_in_years(dob, today) == 5


def test_age_in_years_leap_day_dob_in_non_leap_year() -> None:
    dob = date(2020, 2, 29)
    today = date(2027, 2, 28)
    assert age_in_years(dob, today) == 6


def test_age_in_years_leap_day_dob_after_in_leap_year() -> None:
    dob = date(2020, 2, 29)
    today = date(2028, 3, 1)
    assert age_in_years(dob, today) == 8


def test_age_band_boundaries() -> None:
    today = date(2026, 1, 1)
    assert age_band(date(2022, 1, 1), today) == "under_5"
    assert age_band(date(2021, 1, 1), today) == "5_7"
    assert age_band(date(2019, 1, 1), today) == "5_7"
    assert age_band(date(2018, 1, 1), today) == "8_10"
    assert age_band(date(2015, 1, 1), today) == "11_13"
    assert age_band(date(2012, 1, 1), today) == "14_plus"
