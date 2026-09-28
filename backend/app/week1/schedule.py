"""The 7-day week-1 schedule (PRD §6.2, FR-6). Same order for every child — the age band
adjusts content and starting difficulty only, never which activities appear or when."""

from typing import Final

from app.models.sessions import WEEK1_DAYS

SCHEDULE: Final[dict[int, tuple[str, ...]]] = {
    1: ("sensory_setup", "mood_check_in", "stars_not_clouds"),
    2: ("speak_this_line", "name_the_picture", "which_word"),
    3: ("watch_the_pond", "wait_for_the_bell", "read_and_answer"),
    4: ("follow_instructions", "copy_the_pattern", "story_and_questions"),
    5: ("chat_with_a_character", "how_does_she_feel", "what_would_you_do"),
    6: ("about_me", "oops_try_again", "level_choice", "retell_the_story"),
    # Day 7 repeats two Day 1/2 activities as a consistency check (FR-9), plus the
    # optional Distraction garden, before the gate opens.
    7: ("stars_not_clouds", "speak_this_line", "distraction_garden"),
}

assert set(SCHEDULE) == set(range(1, WEEK1_DAYS + 1)), "SCHEDULE must cover every week-1 day"


def activities_for_day(day_index: int) -> tuple[str, ...]:
    try:
        return SCHEDULE[day_index]
    except KeyError:
        raise ValueError(f"day_index must be between 1 and {WEEK1_DAYS}") from None
