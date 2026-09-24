import uuid

from app.models import SkillScore


def make_score(dimension: str, score: float, confidence: float) -> SkillScore:
    return SkillScore(
        child_id=uuid.uuid4(),
        dimension=dimension,
        score=score,
        confidence=confidence,
        is_baseline=False,
        evidence={},
    )
