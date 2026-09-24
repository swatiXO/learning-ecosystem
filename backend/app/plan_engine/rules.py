from collections.abc import Callable
from dataclasses import dataclass

from app.models import SkillScore

LOW_SCORE_THRESHOLD = 40
MIN_CONFIDENCE_FOR_LOW = 0.5


@dataclass
class Profile:
    """Latest skill score per dimension for one child."""

    scores: dict[str, SkillScore]

    def low(self, dimension: str) -> bool:
        score = self.scores.get(dimension)
        if score is None:
            return False
        return score.score < LOW_SCORE_THRESHOLD and score.confidence >= MIN_CONFIDENCE_FOR_LOW

    def sensory_sensitive(self) -> bool:
        return self.low("sensory_regulation")

    @classmethod
    def from_scores(cls, scores: list[SkillScore]) -> "Profile":
        # Expects at most one score per dimension; if duplicates are passed, the last one wins.
        return cls(scores={score.dimension: score for score in scores})


@dataclass(frozen=True)
class Rule:
    name: str
    when: Callable[[Profile], bool]
    add: dict[str, float]


# Thresholds and weights are placeholders pending Phase 0 pilot data (PROJECT.md §6).
RULES: list[Rule] = [
    Rule(
        "low_attention",
        when=lambda p: p.low("sustained_attention") or p.low("impulse_control"),
        add={"focus_attention": 1.0},
    ),
    Rule(
        "speech_need",
        when=lambda p: p.low("articulation") or p.low("expressive_language"),
        add={"speech_language": 1.0},
    ),
    Rule(
        "social_need",
        when=lambda p: p.low("social_communication") or p.low("emotion_recognition"),
        add={"social_emotional": 1.0},
    ),
    Rule(
        "confidence_need",
        when=lambda p: p.low("self_confidence"),
        add={"confidence_builder": 1.0},
    ),
    Rule("sensory_need", when=lambda p: p.sensory_sensitive(), add={"routine_sensory": 0.5}),
]
