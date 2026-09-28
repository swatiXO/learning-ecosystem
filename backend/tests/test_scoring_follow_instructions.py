import uuid

from app.scoring.follow_instructions import score_follow_instructions
from tests.fixtures.events import make_event


def test_no_valid_responses_returns_no_scores() -> None:
    assert score_follow_instructions([], uuid.uuid4()) == []


def test_perfect_completion_no_hints_scores_100_both_dimensions() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "follow_instructions",
            "response",
            {"n_steps": 3, "steps_followed": 3, "reaction_ms": 800},
        )
        for _ in range(5)
    ]

    scores = score_follow_instructions(events, child_id)
    by_dim = {s.dimension: s for s in scores}

    assert by_dim["auditory_comprehension"].score == 100.0
    assert by_dim["working_memory"].score == 100.0


def test_missed_steps_and_hints_lower_respective_scores() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "follow_instructions",
            "response",
            {"n_steps": 4, "steps_followed": 2, "reaction_ms": 800},
        )
        for _ in range(5)
    ] + [make_event(child_id, "follow_instructions", "hint", {}) for _ in range(2)]

    scores = score_follow_instructions(events, child_id)
    by_dim = {s.dimension: s for s in scores}

    assert by_dim["auditory_comprehension"].score == 50.0
    assert by_dim["working_memory"].score == 60.0  # 1 - 2/5 hints
