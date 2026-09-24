from app.plan_engine.engine import build_plan
from app.plan_engine.rules import Profile
from tests.fixtures.skill_scores import make_score


def test_no_scores_falls_back() -> None:
    result = build_plan(Profile.from_scores([]))

    assert result.modules == {"confidence_builder": 0.5, "focus_attention": 0.5}
    assert result.rules_fired == ["fallback_no_rules_fired"]


def test_low_score_without_confidence_does_not_fire() -> None:
    scores = [make_score("sustained_attention", 20, confidence=0.2)]
    result = build_plan(Profile.from_scores(scores))

    assert result.rules_fired == ["fallback_no_rules_fired"]


def test_single_rule_fires() -> None:
    scores = [make_score("sustained_attention", 20, confidence=0.8)]
    result = build_plan(Profile.from_scores(scores))

    assert result.rules_fired == ["low_attention"]
    assert result.modules == {"focus_attention": 1.0}


def test_top_three_modules_kept_and_normalized() -> None:
    scores = [
        make_score(
            "sustained_attention", 20, confidence=0.8
        ),  # low_attention -> focus_attention 1.0
        make_score("articulation", 20, confidence=0.8),  # speech_need -> speech_language 1.0
        make_score(
            "self_confidence", 20, confidence=0.8
        ),  # confidence_need -> confidence_builder 1.0
        make_score("sensory_regulation", 20, confidence=0.8),  # sensory_need -> routine_sensory 0.5
    ]
    result = build_plan(Profile.from_scores(scores))

    # All 4 rules fired (rationale is transparent about this even though one module got trimmed)
    assert set(result.rules_fired) == {
        "low_attention",
        "speech_need",
        "confidence_need",
        "sensory_need",
    }
    # Only the top 3 by weight survive; routine_sensory (weight 0.5) is the lowest, so it's dropped
    assert len(result.modules) == 3
    assert "routine_sensory" not in result.modules
    assert abs(sum(result.modules.values()) - 1.0) < 0.01


def test_high_confident_scores_do_not_fire_rules() -> None:
    scores = [
        make_score(dim, 90, confidence=0.9) for dim in ("sustained_attention", "impulse_control")
    ]
    result = build_plan(Profile.from_scores(scores))

    assert result.rules_fired == ["fallback_no_rules_fired"]
