import uuid

from app.scoring.watch_the_pond import score_watch_the_pond
from tests.fixtures.events import make_event


def _response(child_id: uuid.UUID, bucket: int, correct: bool) -> object:
    return make_event(
        child_id, "watch_the_pond", "response", {"time_bucket": bucket, "correct": correct}
    )


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_watch_the_pond([], uuid.uuid4()) == []


def test_perfect_accuracy_scores_100() -> None:
    child_id = uuid.uuid4()
    events = [_response(child_id, i, True) for i in range(10)]

    scores = score_watch_the_pond(events, child_id)

    assert scores[0].dimension == "sustained_attention"
    assert scores[0].score == 100.0


def test_fading_accuracy_scores_lower_than_steady_accuracy() -> None:
    child_id = uuid.uuid4()
    fading = [_response(child_id, i, i < 5) for i in range(10)]  # correct early, wrong late
    steady = [_response(child_id, i, True) for i in range(10)]

    fading_score = score_watch_the_pond(fading, child_id)[0].score
    steady_score = score_watch_the_pond(steady, child_id)[0].score

    assert fading_score < steady_score
