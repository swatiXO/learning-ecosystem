"""Module -> activity catalog (PRD FR-18: "each module a set of activities tagged by
skill and difficulty"). Derived directly from PROJECT.md §6's skill-dimension table and
the RULES in plan_engine/rules.py — not invented independently of what's already decided
elsewhere in the project.

Draft, same caveat as docs/activity-signal-map.md: this is engineering's best grounded
default, not a Phase 0 sign-off. It also doesn't handle day-to-day rotation, pacing, or
difficulty tagging — every activity for every module a plan weights comes back, every
time, until someone builds that.
"""

from typing import Final

MODULE_ACTIVITIES: Final[dict[str, tuple[str, ...]]] = {
    # focus_attention <- sustained_attention, impulse_control (rules.py: "low_attention")
    "focus_attention": ("stars_not_clouds", "watch_the_pond", "wait_for_the_bell"),
    # speech_language <- articulation, expressive_language (rules.py: "speech_need")
    "speech_language": (
        "speak_this_line",
        "name_the_picture",
        "which_word",
        "retell_the_story",
    ),
    # social_emotional <- social_communication, emotion_recognition (rules.py: "social_need")
    "social_emotional": ("chat_with_a_character", "how_does_she_feel", "what_would_you_do"),
    # confidence_builder <- self_confidence (rules.py: "confidence_need")
    "confidence_builder": ("about_me", "oops_try_again", "level_choice"),
    # routine_sensory <- sensory_regulation (rules.py: "sensory_need")
    "routine_sensory": ("sensory_setup", "mood_check_in"),
}


def activities_for_modules(modules: dict[str, float]) -> list[str]:
    seen: set[str] = set()
    activities: list[str] = []
    for module in modules:
        for activity in MODULE_ACTIVITIES.get(module, ()):
            if activity not in seen:
                seen.add(activity)
                activities.append(activity)
    return activities
