import uuid

from app.scoring.distraction_garden import score_distraction_garden
from tests.fixtures.events import make_event


def test_no_taps_returns_no_scores() -> None:
    assert score_distraction_garden([], uuid.uuid4()) == []


def test_all_on_task_scores_100() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "distraction_garden", "tap", {"target": "on_task"}) for _ in range(10)
    ]

    scores = score_distraction_garden(events, child_id)

    assert scores[0].dimension == "distractibility"
    assert scores[0].score == 100.0


def test_distractor_taps_lower_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "distraction_garden", "tap", {"target": "distractor"})
        for _ in range(3)
    ] + [make_event(child_id, "distraction_garden", "tap", {"target": "on_task"}) for _ in range(7)]

    scores = score_distraction_garden(events, child_id)

    assert scores[0].score == 70.0
    assert scores[0].evidence["off_task_taps"] == 3
