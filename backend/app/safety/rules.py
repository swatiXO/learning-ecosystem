"""Serious-signal rule definitions (PRD FR-26). A rule firing only ever produces a
SafetyFlag for a human to review later - rule #8/FR-27: the system never contacts anyone,
overrides a plan, or changes a score by itself just because a rule fired.
"""

from dataclasses import dataclass

from app.plan_engine.rules import Profile

# Deliberately much stricter than plan_engine's LOW_SCORE_THRESHOLD (40): that threshold
# is expected to fire often (it drives normal module selection). A safety signal needs to
# be rare. PLACEHOLDER pending Phase 0 clinical input and pilot data, same caveat
# PROJECT.md already puts on plan_engine's thresholds.
VERY_LOW_SCORE_THRESHOLD = 15.0
MIN_CONFIDENCE_FOR_VERY_LOW = 0.5


def _very_low(profile: Profile, dimension: str) -> bool:
    score = profile.scores.get(dimension)
    return (
        score is not None
        and score.score < VERY_LOW_SCORE_THRESHOLD
        and score.confidence >= MIN_CONFIDENCE_FOR_VERY_LOW
    )


@dataclass(frozen=True)
class Rule:
    name: str
    dimension: str


# Every rule here is the same shape (one dimension, very low, confident) so there's no
# per-rule predicate to define yet - add a `when` callable (like plan_engine.rules.Rule)
# the day a rule needs to combine dimensions or look outside skill scores.
RULES: list[Rule] = [
    Rule("very_low_self_confidence", dimension="self_confidence"),
    Rule("very_low_emotion_recognition", dimension="emotion_recognition"),
    Rule("very_low_sensory_regulation", dimension="sensory_regulation"),
]


def evaluate(profile: Profile) -> list[Rule]:
    """Every safety rule that fires for this profile."""
    return [rule for rule in RULES if _very_low(profile, rule.dimension)]
