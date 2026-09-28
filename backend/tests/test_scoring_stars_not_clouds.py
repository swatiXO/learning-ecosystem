import uuid
from datetime import UTC, datetime

from app.models import SignalEvent
from app.scoring.stars_not_clouds import score_stars_not_clouds
from tests.fixtures.stars_not_clouds_events import make_tap


def _tap_with_missing_target(child_id: uuid.UUID) -> SignalEvent:
    return SignalEvent(
        event_id=uuid.uuid4(),
        child_id=child_id,
        session_id=uuid.uuid4(),
        activity_run_id=uuid.uuid4(),
        activity="stars_not_clouds",
        activity_version="1.0.0",
        event_type="tap",
        ts_client=datetime.now(UTC),
        payload={"reaction_ms": 400},
    )


def test_no_taps_returns_no_scores() -> None:
    assert score_stars_not_clouds([], uuid.uuid4()) == []


def test_perfect_impulse_control() -> None:
    child_id = uuid.uuid4()
    events = [make_tap(child_id, "star", 400) for _ in range(10)]

    scores = score_stars_not_clouds(events, child_id)

    impulse = next(s for s in scores if s.dimension == "impulse_control")
    assert impulse.score == 100.0
    assert impulse.confidence == 0.5  # 10 of 20 trials needed for full confidence


def test_false_alarms_lower_impulse_control_score() -> None:
    child_id = uuid.uuid4()
    events = [make_tap(child_id, "star", 400) for _ in range(5)] + [
        make_tap(child_id, "cloud", 350) for _ in range(5)
    ]

    scores = score_stars_not_clouds(events, child_id)

    impulse = next(s for s in scores if s.dimension == "impulse_control")
    assert impulse.score == 50.0
    assert impulse.evidence["false_alarms"] == 5
    assert impulse.evidence["n_taps"] == 10


def test_sustained_attention_needs_at_least_two_go_responses() -> None:
    child_id = uuid.uuid4()
    events = [make_tap(child_id, "star", 400), make_tap(child_id, "cloud", 300)]

    scores = score_stars_not_clouds(events, child_id)

    assert {s.dimension for s in scores} == {"impulse_control"}


def test_sustained_attention_scores_reaction_time_consistency() -> None:
    child_id = uuid.uuid4()
    consistent = [make_tap(child_id, "star", 400) for _ in range(10)]
    variable = [
        make_tap(child_id, "star", ms) for ms in [200, 900, 250, 850, 300, 800, 220, 880, 260, 820]
    ]

    consistent_score = next(
        s.score
        for s in score_stars_not_clouds(consistent, child_id)
        if s.dimension == "sustained_attention"
    )
    variable_score = next(
        s.score
        for s in score_stars_not_clouds(variable, child_id)
        if s.dimension == "sustained_attention"
    )

    assert consistent_score > variable_score


def test_malformed_target_excluded_not_just_from_numerator() -> None:
    child_id = uuid.uuid4()
    # 5 genuine false alarms, plus 5 taps with an unusable target (typo'd, or missing entirely).
    # Before the fix these still counted in the denominator, deflating the false-alarm rate.
    events = (
        [make_tap(child_id, "cloud", 350) for _ in range(5)]
        + [make_tap(child_id, "banana", 400) for _ in range(3)]
        + [_tap_with_missing_target(child_id) for _ in range(2)]
    )

    scores = score_stars_not_clouds(events, child_id)

    impulse = next(s for s in scores if s.dimension == "impulse_control")
    assert impulse.score == 0.0
    assert impulse.evidence["n_taps"] == 5


def test_is_baseline_flag_propagates() -> None:
    child_id = uuid.uuid4()
    events = [make_tap(child_id, "star", 400) for _ in range(3)]

    scores = score_stars_not_clouds(events, child_id, is_baseline=True)

    assert all(s.is_baseline for s in scores)
