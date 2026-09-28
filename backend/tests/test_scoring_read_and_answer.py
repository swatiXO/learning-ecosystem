import uuid

from app.scoring.read_and_answer import score_read_and_answer
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_read_and_answer([], uuid.uuid4()) == []


def test_accuracy_and_time_on_task_captured() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "read_and_answer",
            "response",
            {"correct": True, "time_on_task_ms": 2000},
        ),
        make_event(
            child_id,
            "read_and_answer",
            "response",
            {"correct": False, "time_on_task_ms": 4000},
        ),
    ]

    scores = score_read_and_answer(events, child_id)

    assert scores[0].dimension == "reading_comprehension"
    assert scores[0].score == 50.0
    assert scores[0].evidence["avg_time_on_task_ms"] == 3000.0
