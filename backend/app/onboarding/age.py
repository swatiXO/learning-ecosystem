from datetime import date

# Placeholder, pending open decision D2 (target age range). Bands are (min_age, max_age,
# band_key); max_age=None means "and up".
AGE_BANDS: tuple[tuple[int, int | None, str], ...] = (
    (0, 4, "under_5"),
    (5, 7, "5_7"),
    (8, 10, "8_10"),
    (11, 13, "11_13"),
    (14, None, "14_plus"),
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
