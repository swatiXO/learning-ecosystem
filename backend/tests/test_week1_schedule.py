import pytest

from app.models.sessions import WEEK1_DAYS
from app.schemas.events import REGISTERED_ACTIVITIES
from app.week1.schedule import SCHEDULE, activities_for_day


def test_schedule_covers_every_week1_day() -> None:
    assert set(SCHEDULE) == set(range(1, WEEK1_DAYS + 1))


def test_schedule_activities_are_all_registered() -> None:
    for day, activities in SCHEDULE.items():
        for activity in activities:
            assert activity in REGISTERED_ACTIVITIES, f"day {day}: {activity!r} not registered"


def test_day_7_repeats_a_day_1_and_day_2_activity() -> None:
    # FR-9: day 7 repeats two activities as a consistency check before the gate opens.
    assert "stars_not_clouds" in SCHEDULE[7]
    assert "speak_this_line" in SCHEDULE[7]


@pytest.mark.parametrize("day_index", [0, 8])
def test_activities_for_day_rejects_out_of_range(day_index: int) -> None:
    with pytest.raises(ValueError):
        activities_for_day(day_index)
