from app.plan_engine.rules import Profile
from app.safety.rules import evaluate
from tests.fixtures.skill_scores import make_score


def test_no_scores_fires_no_rules() -> None:
    assert evaluate(Profile.from_scores([])) == []


def test_very_low_confident_score_fires_its_rule() -> None:
    scores = [make_score("self_confidence", 5, confidence=0.8)]
    fired = evaluate(Profile.from_scores(scores))
    assert [rule.name for rule in fired] == ["very_low_self_confidence"]


def test_low_but_not_very_low_score_does_not_fire() -> None:
    # 30 is "low" enough to drive plan_engine's module selection, but well above this
    # module's much stricter safety threshold (15).
    scores = [make_score("self_confidence", 30, confidence=0.8)]
    assert evaluate(Profile.from_scores(scores)) == []


def test_very_low_score_without_confidence_does_not_fire() -> None:
    scores = [make_score("self_confidence", 5, confidence=0.2)]
    assert evaluate(Profile.from_scores(scores)) == []


def test_dimension_outside_the_rule_set_never_fires() -> None:
    # sustained_attention has no safety rule at all, however low it scores.
    scores = [make_score("sustained_attention", 1, confidence=0.9)]
    assert evaluate(Profile.from_scores(scores)) == []


def test_multiple_rules_can_fire_independently() -> None:
    scores = [
        make_score("self_confidence", 5, confidence=0.8),
        make_score("emotion_recognition", 5, confidence=0.8),
    ]
    fired = {rule.name for rule in evaluate(Profile.from_scores(scores))}
    assert fired == {"very_low_self_confidence", "very_low_emotion_recognition"}
