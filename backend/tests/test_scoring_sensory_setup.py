import uuid

from app.scoring.sensory_setup import score_sensory_setup
from tests.fixtures.events import make_event


def test_no_settings_changed_returns_no_scores() -> None:
    assert score_sensory_setup([], uuid.uuid4()) == []


def test_frequent_calm_mode_use_lowers_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id, "sensory_setup", "setting_changed", {"setting": "calm_mode", "value": "on"}
        )
        for _ in range(5)
    ]

    scores = score_sensory_setup(events, child_id)

    assert scores[0].dimension == "sensory_regulation"
    assert scores[0].score == 50.0
    assert scores[0].evidence["calm_mode_activations"] == 5


def test_non_calm_mode_settings_do_not_lower_the_score() -> None:
    child_id = uuid.uuid4()
    events = [
        make_event(
            child_id,
            "sensory_setup",
            "setting_changed",
            {"setting": "volume", "value": "low"},
        )
        for _ in range(3)
    ]

    scores = score_sensory_setup(events, child_id)

    assert scores[0].score == 100.0
