import uuid

from app.scoring.which_word import score_which_word
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_which_word([], uuid.uuid4()) == []


def test_correctness_derived_from_target_matching_selected() -> None:
    child_id = uuid.uuid4()
    events = [
        # Client claims "correct": False but target == selected, so it's actually right —
        # server-authoritative scoring must not trust the client's own flag.
        make_event(
            child_id,
            "which_word",
            "response",
            {"target": "ship", "selected": "ship", "correct": False, "reaction_ms": 500},
        ),
        make_event(
            child_id,
            "which_word",
            "response",
            {"target": "chip", "selected": "ship", "correct": True, "reaction_ms": 600},
        ),
    ]

    scores = score_which_word(events, child_id)

    assert scores[0].dimension == "articulation"
    assert scores[0].score == 50.0
    assert scores[0].evidence["correct"] == 1
