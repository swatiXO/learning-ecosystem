import uuid

from app.scoring.wait_for_the_bell import score_wait_for_the_bell
from tests.fixtures.events import make_event


def test_no_taps_returns_no_scores() -> None:
    assert score_wait_for_the_bell([], uuid.uuid4()) == []


def test_no_early_taps_scores_100() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "wait_for_the_bell", "tap", {"early": False, "wait_ms": 1200})
        for _ in range(10)
    ]

    scores = score_wait_for_the_bell(events, child_id)

    assert scores[0].dimension == "impulse_control"
    assert scores[0].score == 100.0
    assert scores[0].evidence["avg_wait_ms"] == 1200.0


def test_early_taps_lower_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "wait_for_the_bell", "tap", {"early": True, "wait_ms": None})
        for _ in range(5)
    ] + [
        make_event(child_id, "wait_for_the_bell", "tap", {"early": False, "wait_ms": 900})
        for _ in range(5)
    ]

    scores = score_wait_for_the_bell(events, child_id)

    assert scores[0].score == 50.0
    assert scores[0].evidence["early_taps"] == 5
