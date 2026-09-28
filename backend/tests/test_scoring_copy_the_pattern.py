import uuid

from app.scoring.copy_the_pattern import score_copy_the_pattern
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_copy_the_pattern([], uuid.uuid4()) == []


def test_longest_correct_sequence_drives_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "copy_the_pattern",
            "response",
            {"sequence_length": length, "correct_order": True},
        )
        for length in [2, 5, 3]
    ]

    scores = score_copy_the_pattern(events, child_id)

    assert scores[0].dimension == "working_memory"
    assert scores[0].score == 50.0  # longest=5 / max=10
    assert scores[0].evidence["longest_correct_sequence"] == 5


def test_incorrect_order_does_not_count_toward_longest() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "copy_the_pattern",
            "response",
            {"sequence_length": 9, "correct_order": False},
        ),
        make_event(
            child_id,
            "copy_the_pattern",
            "response",
            {"sequence_length": 3, "correct_order": True},
        ),
    ]

    scores = score_copy_the_pattern(events, child_id)

    assert scores[0].evidence["longest_correct_sequence"] == 3
