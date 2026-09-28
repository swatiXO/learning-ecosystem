import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "copy_the_pattern"
# Placeholder scaling: a longest correct sequence of 10 maps to a perfect score.
MAX_SCORED_SEQUENCE_LENGTH = 10


def score_copy_the_pattern(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [
        e
        for e in responses
        if isinstance(e.payload.get("sequence_length"), int)
        and isinstance(e.payload.get("correct_order"), bool)
    ]
    if not valid:
        return []

    correct = [e for e in valid if e.payload["correct_order"]]
    longest_correct = max((e.payload["sequence_length"] for e in correct), default=0)
    order_error_rate = 1 - len(correct) / len(valid)

    score = min(100.0, 100.0 * longest_correct / MAX_SCORED_SEQUENCE_LENGTH)

    return [
        SkillScore(
            child_id=child_id,
            dimension="working_memory",
            score=round(score, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
                "longest_correct_sequence": longest_correct,
                "order_error_rate": round(order_error_rate, 2),
            },
        )
    ]
