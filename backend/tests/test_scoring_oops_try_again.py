import uuid

from app.scoring.oops_try_again import score_oops_try_again
from tests.fixtures.events import make_event


def test_no_retries_or_quits_returns_no_scores() -> None:
    assert score_oops_try_again([], uuid.uuid4()) == []


def test_retries_score_higher_than_quits() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "oops_try_again", "retry", {"time_to_retry_ms": 1000})
        for _ in range(3)
    ] + [make_event(child_id, "oops_try_again", "quit", {}) for _ in range(1)]

    scores = score_oops_try_again(events, child_id)

    assert scores[0].dimension == "self_confidence"
    assert scores[0].score == 75.0
    assert scores[0].evidence["avg_time_to_retry_ms"] == 1000.0
