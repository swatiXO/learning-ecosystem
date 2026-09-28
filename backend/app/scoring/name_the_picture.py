import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "name_the_picture"
# Placeholder scaling: 2000ms of word-finding time costs 100 points, floored at 0.
MS_PER_SCORE_POINT = 20.0


def score_name_the_picture(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    """Only word-finding time -> expressive_language. Articulation itself needs the
    Phase 3 speech pipeline to analyze the captured audio — not computable here yet."""
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [
        e
        for e in responses
        if isinstance(e.payload.get("reaction_ms"), (int, float)) and e.payload["reaction_ms"] >= 0
    ]
    if not valid:
        return []

    reaction_times = [e.payload["reaction_ms"] for e in valid]
    avg_reaction_ms = sum(reaction_times) / len(reaction_times)
    score = max(0.0, 100.0 - avg_reaction_ms / MS_PER_SCORE_POINT)

    return [
        SkillScore(
            child_id=child_id,
            dimension="expressive_language",
            score=round(score, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
                "avg_word_finding_ms": round(avg_reaction_ms, 1),
            },
        )
    ]
