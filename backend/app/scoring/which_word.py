import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "which_word"


def score_which_word(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    # Correctness is derived from target == selected, not the client's own `correct` flag
    # — same server-authoritative principle as stars_not_clouds.
    valid = [
        e
        for e in responses
        if isinstance(e.payload.get("target"), str) and isinstance(e.payload.get("selected"), str)
    ]
    if not valid:
        return []

    correct = [e for e in valid if e.payload["target"] == e.payload["selected"]]
    accuracy = len(correct) / len(valid)

    return [
        SkillScore(
            child_id=child_id,
            dimension="articulation",
            score=round(100.0 * accuracy, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
                "correct": len(correct),
            },
        )
    ]
