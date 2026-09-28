import uuid
from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import SignalEvent, SkillScore
from app.scoring import (
    copy_the_pattern,
    distraction_garden,
    follow_instructions,
    how_does_she_feel,
    mood_check_in,
    name_the_picture,
    oops_try_again,
    read_and_answer,
    sensory_setup,
    stars_not_clouds,
    story_and_questions,
    wait_for_the_bell,
    watch_the_pond,
    which_word,
)

Extractor = Callable[[list[SignalEvent], uuid.UUID, bool], list[SkillScore]]

# Not every activity has an extractor yet — some are blocked on the Phase 3 speech
# pipeline (speak_this_line, retell_the_story, chat_with_a_character's "on topic" signal)
# or a content-design rubric that doesn't exist (what_would_you_do, about_me,
# level_choice's risk-taking signal). See docs/activity-signal-map.md and issue #29.
EXTRACTORS: list[tuple[str, Extractor]] = [
    (stars_not_clouds.ACTIVITY, stars_not_clouds.score_stars_not_clouds),
    (watch_the_pond.ACTIVITY, watch_the_pond.score_watch_the_pond),
    (wait_for_the_bell.ACTIVITY, wait_for_the_bell.score_wait_for_the_bell),
    (distraction_garden.ACTIVITY, distraction_garden.score_distraction_garden),
    (follow_instructions.ACTIVITY, follow_instructions.score_follow_instructions),
    (copy_the_pattern.ACTIVITY, copy_the_pattern.score_copy_the_pattern),
    (story_and_questions.ACTIVITY, story_and_questions.score_story_and_questions),
    (read_and_answer.ACTIVITY, read_and_answer.score_read_and_answer),
    (which_word.ACTIVITY, which_word.score_which_word),
    (name_the_picture.ACTIVITY, name_the_picture.score_name_the_picture),
    (how_does_she_feel.ACTIVITY, how_does_she_feel.score_how_does_she_feel),
    (oops_try_again.ACTIVITY, oops_try_again.score_oops_try_again),
    (mood_check_in.ACTIVITY, mood_check_in.score_mood_check_in),
    (sensory_setup.ACTIVITY, sensory_setup.score_sensory_setup),
]


def recompute_scores(
    db: Session, child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    new_scores: list[SkillScore] = []
    for activity, extractor in EXTRACTORS:
        events = db.scalars(
            select(SignalEvent).where(
                SignalEvent.child_id == child_id, SignalEvent.activity == activity
            )
        ).all()
        new_scores.extend(extractor(list(events), child_id, is_baseline=is_baseline))

    db.add_all(new_scores)
    db.flush()
    return new_scores
