import uuid

from app.scoring.mood_check_in import score_mood_check_in
from tests.fixtures.events import make_event


def test_no_events_returns_no_scores() -> None:
    assert score_mood_check_in([], uuid.uuid4()) == []


def test_skips_lower_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "mood_check_in", "mood", {"mood": "happy", "phase": "before"})
        for _ in range(3)
    ] + [make_event(child_id, "mood_check_in", "skip", {}) for _ in range(1)]

    scores = score_mood_check_in(events, child_id)

    assert scores[0].dimension == "sensory_regulation"
    assert scores[0].score == 75.0
    assert scores[0].evidence["skips"] == 1
