import uuid

from app.scoring.story_and_questions import score_story_and_questions
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_story_and_questions([], uuid.uuid4()) == []


def test_accuracy_drives_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(child_id, "story_and_questions", "response", {"correct": True}) for _ in range(3)
    ] + [
        make_event(child_id, "story_and_questions", "response", {"correct": False})
        for _ in range(1)
    ]

    scores = score_story_and_questions(events, child_id)

    assert scores[0].dimension == "auditory_comprehension"
    assert scores[0].score == 75.0
    assert scores[0].evidence["replays_requested"] == 0
