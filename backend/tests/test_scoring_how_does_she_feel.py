import uuid

from app.scoring.how_does_she_feel import score_how_does_she_feel
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_how_does_she_feel([], uuid.uuid4()) == []


def test_accuracy_drives_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "how_does_she_feel", "response", {"correct": True}) for _ in range(4)
    ] + [
        make_event(child_id, "how_does_she_feel", "response", {"correct": False}) for _ in range(1)
    ]

    scores = score_how_does_she_feel(events, child_id)

    assert scores[0].dimension == "emotion_recognition"
    assert scores[0].score == 80.0
