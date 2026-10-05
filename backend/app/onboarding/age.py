from datetime import date

# D2 (decision log 2026-10-05): ages 5-12, bands 5-7 / 8-10 / 11-12. Bands are (min_age,
# max_age, band_key); max_age=None means "and up". Onboarding only accepts 5-12, but a
# child who turns 13 while enrolled stays in the oldest band rather than falling out of
# every band.
AGE_BANDS: tuple[tuple[int, int | None, str], ...] = (
    (5, 7, "5_7"),
    (8, 10, "8_10"),
    (11, None, "11_12"),
)


def age_in_years(dob: date, today: date) -> int:
    years = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        years -= 1
    return years


def age_band(dob: date, today: date) -> str:
    years = age_in_years(dob, today)
    for min_age, max_age, band in AGE_BANDS:
        if years >= min_age and (max_age is None or years <= max_age):
            return band
    return AGE_BANDS[0][2]
