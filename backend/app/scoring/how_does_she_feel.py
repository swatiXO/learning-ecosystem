import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "how_does_she_feel"


def score_how_does_she_feel(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [e for e in responses if isinstance(e.payload.get("correct"), bool)]
    if not valid:
        return []

    accuracy = sum(1 for e in valid if e.payload["correct"]) / len(valid)

    return [
        SkillScore(
            child_id=child_id,
            dimension="emotion_recognition",
            score=round(100.0 * accuracy, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
            },
        )
    ]
