import uuid

from app.scoring.name_the_picture import score_name_the_picture
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_name_the_picture([], uuid.uuid4()) == []


def test_faster_word_finding_scores_higher() -> None:
    child_id = uuid.uuid4()
    fast = [make_event(child_id, "name_the_picture", "response", {"reaction_ms": 500})]
    slow = [make_event(child_id, "name_the_picture", "response", {"reaction_ms": 3000})]

    fast_score = score_name_the_picture(fast, child_id)[0].score
    slow_score = score_name_the_picture(slow, child_id)[0].score

    assert fast_score > slow_score
